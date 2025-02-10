from toolium.behave.environment import (before_all as toolium_before_all, before_feature as toolium_before_feature,
                                        before_scenario as toolium_before_scenario,
                                        after_scenario as toolium_after_scenario,
                                        after_feature as toolium_after_feature, after_all as toolium_after_all)
from toolium.config_files import ConfigFiles
from zapv2 import ZAPv2
import time
import sys

def before_all(context):
    """Initialization method that will be executed before the test execution

    :param context: behave context
    """
    context.config_files = ConfigFiles()
    toolium_before_all(context)


def before_feature(context, feature):
    """Feature initialization

    :param context: behave context
    :param feature: running feature
    """
    toolium_before_feature(context, feature)

    # Get DAST configuration
    context.pscan = context.toolium_config.getboolean_optional('DAST', 'pscan')
    context.ascan = context.toolium_config.getboolean_optional('DAST', 'ascan')
    context.target = context.toolium_config.get('DAST', 'target')
    api_key = context.toolium_config.get('DAST', 'api_key')

    # Initialize ZAProxy
    if context.pscan or context.ascan:
        context.zap = ZAPv2(apikey=api_key)
        if context.ascan:
            context.zap_scan = context.zap.ascan
            context.zap_scan.enable_all_scanners()


def before_scenario(context, scenario):
    """Scenario initialization

    :param context: behave context
    :param scenario: running scenario
    """
    toolium_before_scenario(context, scenario)


def after_scenario(context, scenario):
    """Clean method that will be executed after each scenario

    :param context: behave context
    :param scenario: running scenario
    """
    
    if context.pscan:
        while int(context.zap.pscan.records_to_scan) > 0:
            print('Records to passive scan : ' + context.zap.pscan.records_to_scan)
            time.sleep(1)

    if context.ascan:
        context.zap_scan_id = context.zap.ascan.scan(context.target)
        print('Active Scan progress')
        while int(context.zap.ascan.status(context.zap_scan_id)) < 100:
            scan_count = int(context.zap.ascan.status(context.zap_scan_id))
            progress_bar(scan_count)
            time.sleep(10)
        context.zap_scan_id = None
    
    toolium_after_scenario(context, scenario)


def after_feature(context, feature):
    """Clean method that will be executed after each feature

    :param context: behave context
    :param feature: running feature
    """
    if context.pscan or context.ascan:
        context.fhtml = open(f'output/zapreport.html', 'w')
        context.fhtml.write(context.zap.core.htmlreport())
        context.fhtml.close()
        context.zap.core.delete_all_alerts()

    toolium_after_feature(context, feature)


def after_all(context):
    """Clean method that will be executed after all features are finished

    :param context: behave context
    """
    toolium_after_all(context)

def progress_bar(count_value):
    bar = '=' * (count_value - 1) + '>' + '-' * (100 - count_value)
    sys.stdout.write('[%s] %s\r' % (bar, f'{count_value}%'))
    sys.stdout.flush()