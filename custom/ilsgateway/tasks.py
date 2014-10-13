from decimal import Decimal
from celery import group
from celery.task import task, periodic_task
from couchdbkit.exceptions import ResourceNotFound
from casexml.apps.stock.models import StockReport, StockTransaction
from corehq.apps.commtrack.models import StockState, SupplyPointCase, Product, SQLProduct
from couchforms.models import XFormInstance
from custom.ilsgateway.api import ILSGatewayEndpoint, Location
from custom.ilsgateway.commtrack import bootstrap_domain, sync_ilsgateway_location, commtrack_settings_sync,\
    sync_ilsgateway_product


#@periodic_task(run_every=timedelta(days=1), queue=getattr(settings, 'CELERY_PERIODIC_QUEUE', 'celery'))
from custom.ilsgateway.models import ILSGatewayConfig, SupplyPointStatus, DeliveryGroupReport
from dimagi.utils.dates import force_to_datetime


def migration_task():
    configs = ILSGatewayConfig.get_all_configs()
    for config in configs:
        if config.enabled:
            bootstrap_domain(config)


@task
def bootstrap_domain_task(domain):
    ilsgateway_config = ILSGatewayConfig.for_domain(domain)
    return bootstrap_domain(ilsgateway_config)

# District Moshi-Rural
FACILITIES = [906, 907, 908, 909, 910, 911, 912, 913, 914, 915, 916,
              917, 918, 919, 920, 921, 922, 923, 924, 925, 926, 927,
              928, 929, 930, 931, 932, 933, 934, 935, 936, 937, 938,
              939, 941, 942, 943, 944, 946, 947, 948, 949, 950, 951,
              952, 953, 954, 955, 4860, 654]


def get_locations(domain, endpoint):
    for facility in FACILITIES:
        location = endpoint.get_location(facility)
        sync_ilsgateway_location(domain, endpoint, Location.from_json(location))


@task
def product_stock_task(domain, endpoint):
    for facility in FACILITIES:
        product_stocks = endpoint.get_productstocks(filters=dict(supply_point=facility))[1]
        for product_stock in product_stocks:
            case = SupplyPointCase.view('hqcase/by_domain_external_id',
                                        key=[domain, str(product_stock.supply_point_id)],
                                        reduce=False,
                                        include_docs=True,
                                        limit=1).first()
            product = Product.get_by_code(domain, product_stock.product_code)
            try:
                StockState.objects.get(section_id='stock', case_id=case._id, product_id=product._id)
            except StockState.DoesNotExist:
                StockState.objects.create(section_id='stock',
                                          case_id=case._id,
                                          product_id=product._id,
                                          stock_on_hand=product_stock.quantity or 0,
                                          daily_consumption=product_stock.auto_monthly_consumption or 0,
                                          last_modified_date=product_stock.last_modified,
                                          sql_product=SQLProduct.objects.get(product_id=product._id))


@task
def stock_transaction_task(domain, endpoint):
    # Faking xform
    try:
        xform = XFormInstance.get(docid='ilsgateway-xform')
    except ResourceNotFound:
        xform = XFormInstance(_id='ilsgateway-xform')
        xform.save()

    for facility in FACILITIES:
        stocktransactions = endpoint.get_stocktransactions(filters=(dict(supply_point=facility)))[1]
        for stocktransaction in stocktransactions:
            case = SupplyPointCase.view('hqcase/by_domain_external_id',
                                        key=[domain, str(stocktransaction.supply_point_id)],
                                        reduce=False,
                                        include_docs=True,
                                        limit=1).first()
            product = Product.get_by_code(domain, stocktransaction.product_code)
            try:
                StockTransaction.objects.get(case_id=case._id,
                                             product_id=product._id, report__date=force_to_datetime(stocktransaction.date),
                                             stock_on_hand=Decimal(stocktransaction.ending_balance),
                                             type='stockonhand', report__domain=domain)
            except StockTransaction.DoesNotExist:
                r = StockReport.objects.create(form_id=xform._id, date=force_to_datetime(stocktransaction.date),
                                               type='balance', domain=domain)
                StockTransaction.objects.create(report=r, section_id='stock', case_id=case._id, product_id=product._id,
                                                type='stockonhand', stock_on_hand=Decimal(stocktransaction.ending_balance))


@task
def supply_point_statuses_task(domain, endpoint):
    for facility in FACILITIES:
        supplypointstatuses = endpoint.get_supplypointstatuses(domain, filters=dict(supply_point=facility))[1]
        for sps in supplypointstatuses:
            try:
                SupplyPointStatus.objects.get(status_type=sps.status_type, status_value=sps.status_value,
                                              status_date=sps.status_date, supply_point=sps.supply_point)
            except SupplyPointStatus.DoesNotExist:
                sps.save()


@task
def delivery_group_reports_task(domain, endpoint):
    for facility in FACILITIES:
        deliverygroupreports = endpoint.get_deliverygroupreports(domain, filters=dict(supply_point=facility))[1]
        for dgr in deliverygroupreports:
            try:
                #TODO Avoid duplicating. Should be done better.
                DeliveryGroupReport.objects.get(supply_point=dgr.supply_point,
                                                quantity=dgr.quantity,
                                                report_date=dgr.report_date,
                                                delivery_group=dgr.delivery_group)
            except DeliveryGroupReport.DoesNotExist:
                dgr.save()


@task
def stock_data_task(domain):
    ilsgateway_config = ILSGatewayConfig.for_domain(domain)
    domain = ilsgateway_config.domain
    endpoint = ILSGatewayEndpoint.from_config(ilsgateway_config)
    commtrack_settings_sync(domain)
    for product in endpoint.get_products():
        sync_ilsgateway_product(domain, product)
    get_locations(domain, endpoint)
    group(product_stock_task.delay(domain, endpoint),
          stock_transaction_task.delay(domain, endpoint),
          supply_point_statuses_task.delay(domain, endpoint),
          delivery_group_reports_task.delay(domain, endpoint))