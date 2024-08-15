from datetime import datetime
import pytz
from logger.models import LoggerDebug, LoggerProduction


def logger(respond_data, stage):
    # ---------------------- logs limit handle ---------------------
    number_of_d_object = LoggerDebug.objects.count()
    deviation = number_of_d_object - 50000
    if deviation > 0:
        LoggerDebug.objects.filter(
            id__in=list(LoggerDebug.objects.values_list('pk', flat=True)[:(deviation + 1000)])).delete()
    number_of_p_object = LoggerProduction.objects.count()
    deviation = number_of_p_object - 5000
    if deviation > 0:
        LoggerProduction.objects.filter(
            id__in=list(LoggerProduction.objects.values_list('pk', flat=True)[:(deviation + 100)])).delete()

    th_IR = pytz.timezone('Asia/Tehran')
    datetime_IR = datetime.now(th_IR)
    current_time = datetime_IR.strftime("%H:%M:%S.%f")[:-3]
    if stage == 'p':  # production level
        l_o_g = str(current_time) + " - " + str(respond_data)
        print(l_o_g)
        new_log = LoggerProduction(
            log=l_o_g,
        )
        new_log.save()
        new_log_debug = LoggerDebug(
            log=l_o_g,
        )
        new_log_debug.save()
    elif stage == 'd':  # debug level
        l_o_g = str(current_time) + " - " + str(respond_data)
        print(l_o_g)
        new_log = LoggerDebug(
            log=l_o_g,
        )
        new_log.save()


