resource "aws_s3_bucket" "bucket" {
  bucket = "addi-challenge-evaluation-store"
}

resource "aws_s3_bucket_acl" "bucket_acl" {
  bucket = aws_s3_bucket.bucket.id
  acl    = "private"
}

resource "aws_iam_role" "firehose_role" {
  name = "firehose-role"

  assume_role_policy = <<EOF
{
  "Version": "2012-10-17",
  "Statement": [
    {
      "Action": "sts:AssumeRole",
      "Principal": {
        "Service": "firehose.amazonaws.com"
      },
      "Effect": "Allow",
      "Sid": ""
    }
  ]
}
EOF
}



resource "aws_kinesis_firehose_delivery_stream" "firehose_stream" {
  name        = "evaluation-store-firehose-stream"
  destination = "s3"

  s3_configuration {
    role_arn   = aws_iam_role.firehose_role.arn
    bucket_arn = aws_s3_bucket.bucket.arn
    buffer_interval    = 60
    buffer_size        = 1
  }
}


resource "aws_iam_policy" "firehose_s3" {
  name_prefix = "firehose-policy"
  policy      = <<-EOF
{
  "Version": "2012-10-17",
  "Statement": [
    {
        "Sid": "",
        "Effect": "Allow",
        "Action": [
            "s3:AbortMultipartUpload",
            "s3:GetBucketLocation",
            "s3:GetObject",
            "s3:ListBucket",
            "s3:ListBucketMultipartUploads",
            "s3:PutObject"
        ],
        "Resource": [
            "${aws_s3_bucket.bucket.arn}",
            "${aws_s3_bucket.bucket.arn}/*"
        ]
    }
  ]
}
EOF
}

resource "aws_iam_role_policy_attachment" "firehose_s3" {
  role       = aws_iam_role.firehose_role.name
  policy_arn = aws_iam_policy.firehose_s3.arn
}

# resource "aws_iam_policy" "put_record" {
#   name_prefix = "kinesis-firehose"
#   policy      = <<-EOF
# {
#     "Version": "2012-10-17",
#     "Statement": [
#         {
#             "Effect": "Allow",
#             "Action": [
#                 "firehose:PutRecord",
#                 "firehose:PutRecordBatch"
#             ],
#             "Resource": [
#                 "${aws_kinesis_firehose_delivery_stream.firehose_stream.arn}"
#             ]
#         }
#     ]
# }
# EOF
# }

resource "aws_athena_database" "evaluation_store_table" {
  name   = "evaluation_store_table"
  bucket = aws_s3_bucket.bucket.bucket
}