CREATE EXTERNAL TABLE IF NOT EXISTS `evaluation_store_table`.`showcase_mlops_feature_model_evaluation_store_v1` (
  `event_id` string,
  `model_name` string,
  `model_version` string,
  `features` map<string,string>,
  `created_at` string,
  `prediction` string,
  `pk`string


)
ROW FORMAT SERDE 'org.apache.hive.hcatalog.data.JsonSerDe'
WITH SERDEPROPERTIES ('serialization.format' = '1')
LOCATION 's3://company-showcase-evaluation-store/'
TBLPROPERTIES ('has_encrypted_data' = 'false');