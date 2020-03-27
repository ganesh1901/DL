import datetime


class Others:
    def __init__(self):
        self.log_filename = "../out/app_log.log"
        self.log_fd = open(self.log_filename, "a")

    def GetDateTime(self):
        curr_time_object = datetime.datetime.now()
        curr_time = "%02d-%02d-%02d %02d:%02d:%02d" % (
            curr_time_object.day, curr_time_object.month, curr_time_object.year, curr_time_object.hour,
            curr_time_object.minute, curr_time_object.second)
        return curr_time

    def LogDebug(self, buff):
        self.log_fd.write('DEBUG:\t')
        self.log_fd.write(self.GetDateTime() + ' ')
        self.log_fd.write(buff)
        self.log_fd.write('\n')

    def LogWarn(self, buff):
        self.log_fd.write('WARN:\t')
        self.log_fd.write(self.GetDateTime() + ' ')
        self.log_fd.write(buff)
        self.log_fd.write('\n')