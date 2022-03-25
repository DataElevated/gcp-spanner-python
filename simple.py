from google.cloud import spanner
from google.cloud.spanner_v1 import param_types

# Instantiate Spanner Client
SpannerClient = spanner.Client()
InstanceID = ''
Instance = SpannerClient.instance(InstanceID)
Instance