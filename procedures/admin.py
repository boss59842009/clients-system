from django.contrib import admin
from procedures.models import ProcedureModel, MasterModel, MasterProcedureModel, MasterScheduleModel

admin.site.register(MasterProcedureModel)
admin.site.register(MasterScheduleModel)
admin.site.register(ProcedureModel)
admin.site.register(MasterModel)
