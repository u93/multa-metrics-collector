import metric_validations
from marshmallow import Schema, fields, validates_schema, ValidationError, validates, validate, post_load


DATE_FORMAT = metric_validations.DATE_FORMAT

analysis_list = metric_validations.analysis_list["DISK"]

agent_list = metric_validations.agent_list

metrics_list = metrics_list = metric_validations.metric_list["DISK"]

class ParametersSchema(Schema):
    metric_value = fields.List(fields.String(), required = True)
    metric_range = fields.String(allow_none=True)
    start_time = fields.Time(allow_none=True)
    end_time = fields.Time(allow_none=True)
    start_date = fields.Date(DATE_FORMAT, allow_none=True)
    end_date = fields.Date(DATE_FORMAT, allow_none=True)
    start_timestamp = fields.Integer(allow_none=True)
    end_timestamp = fields.Integer(allow_none=True)
    agents = fields.List(fields.String(), required = True)
    metadata = fields.Dict()

    @validates("metric_value")
    def validate_metric_value(self, metric_value):
        for metric in metric_value:
            if metric not in metrics_list:
                raise ValidationError('invalid metric value')

    @validates("agents")
    def validate_agents(self, agents):
        for agent in agents:
            if agent not in agent_list:
                raise ValidationError('invalid agent')

    @validates_schema
    def validate_time_input(self, data, **kwards):
        if data["start_timestamp"] != None and data["end_timestamp"] == None:
            raise ValidationError("end_timestamp field is required")
        if data["start_timestamp"] == None and data["end_timestamp"] != None:
            raise ValidationError("start_timestamp field is required")
        if data["start_date"] != None and data["end_date"] == None:
            raise ValidationError("start_date field is required")
        if data["start_date"] == None and data["end_date"] != None:
            raise ValidationError("end_date field is required")
                

    @validates_schema
    def validate_timestamp(self, data, **kwards):
        if data["start_timestamp"] != None and data["end_timestamp"] != None:
            if data["start_timestamp"] > data["end_timestamp"]:
                raise ValidationError("timestamp order error")

    @validates_schema
    def validate_date(self, data, **kwards):
        if data["start_date"] != None and data["end_date"] != None:
            if data["start_date"] > data["end_date"]:
                raise ValidationError("date order error")

    @validates_schema
    def validate_time(self, data, **kwards):
        if data["start_time"] != None and data["end_time"] != None:
            if data["start_time"] > data["end_time"]:
                raise ValidationError("time order error")


class DiskSchema(Schema):
	analysis = fields.String()
	parameters = fields.Nested(ParametersSchema)

	@validates("analysis")
	def validate_analysis(self, analysis):
	    if analysis not in analysis_list:
	        raise ValidationError('analysis not available')
