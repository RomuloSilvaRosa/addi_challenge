



resource "aws_iam_role" "iam-lambda-orchestrator" {
  name = "orchestrator-role"

  assume_role_policy = <<EOF
{
  "Version": "2012-10-17",
  "Statement": [
    {
      "Action": "sts:AssumeRole",
      "Principal": {
        "Service": "lambda.amazonaws.com"
      },
      "Effect": "Allow",
      "Sid": ""
    }
  ]
}
EOF
}


resource "aws_iam_policy" "lambda_orch_cloudwatch" {
  name_prefix = "lambda-cloudwatch-policy"
  policy      = <<-EOF
{
    "Statement": [
        {
            "Action": [
                "logs:CreateLogGroup",
                "logs:CreateLogStream",
                "logs:PutLogEvents"
            ],
            "Effect": "Allow",
            "Resource": "arn:aws:logs:*:*:*"
        } 
    ],
    "Version": "2012-10-17"
}
EOF
}

resource "aws_iam_policy" "lambda_orch_dynamo" {
  name_prefix = "lambda-dynamo-policy"
  policy      = <<-EOF
{
    "Statement": [
        {
            "Action": [
                "dynamodb:GetItem"
            ],
            "Effect": "Allow",
            "Resource": "${aws_dynamodb_table.feature-store-credit-card-dynamodb-table.arn}"
        }
    ],
    "Version": "2012-10-17"
}
EOF
}

resource "aws_iam_policy" "lambda_orch_lambda" {
  name_prefix = "lambda-invoke-another-lambda-policy"
  policy      = <<-EOF
{
    "Statement": [
        {
            "Action": [
                "lambda:InvokeFunction"
            ],
            "Effect": "Allow",
            "Resource": "${aws_lambda_function.model-lambda.arn}"
        }
    ],
    "Version": "2012-10-17"
}
EOF
}

resource "aws_iam_policy" "lambda_orch_firehose" {
  name_prefix = "lambda-invoke-another-lambda-policy"
  policy      = <<-EOF
{
    "Statement": [
        {

            "Action": [
                "firehose:PutRecord"
            ],
            "Effect": "Allow",
            "Resource": "${aws_kinesis_firehose_delivery_stream.firehose_stream.arn}"
        }
    ],
    "Version": "2012-10-17"
}
EOF
}

resource "aws_iam_role_policy_attachment" "lambda_orch_role_cloud" {
  role       = aws_iam_role.iam-lambda-orchestrator.name
  policy_arn = aws_iam_policy.lambda_orch_cloudwatch.arn
}

resource "aws_iam_role_policy_attachment" "lambda_orch_role_fire" {
  role       = aws_iam_role.iam-lambda-orchestrator.name
  policy_arn = aws_iam_policy.lambda_orch_firehose.arn
}

resource "aws_iam_role_policy_attachment" "lambda_orch_role_dynamo" {
  role       = aws_iam_role.iam-lambda-orchestrator.name
  policy_arn = aws_iam_policy.lambda_orch_dynamo.arn
}
resource "aws_iam_role_policy_attachment" "lambda_orch_role_lambda" {
  role       = aws_iam_role.iam-lambda-orchestrator.name
  policy_arn = aws_iam_policy.lambda_orch_lambda.arn
}



resource "aws_ecr_repository" "orchestrator-ecr" {
  name                 = "orchestrator/lambda"
  image_tag_mutability = "MUTABLE"

  image_scanning_configuration {
    scan_on_push = true
  }
  provisioner "local-exec" {
    command = <<-EOT
      docker pull alpine
      aws ecr get-login-password | docker login --username AWS --password-stdin ${aws_ecr_repository.orchestrator-ecr.repository_url}
      docker tag alpine "${aws_ecr_repository.orchestrator-ecr.repository_url}:latest"
      docker push "${aws_ecr_repository.orchestrator-ecr.repository_url}:latest"
    EOT
  }
}

resource "aws_lambda_function" "orchestrator-lambda" {
  function_name = "addi-challenge-orchestrator"
  image_uri     = "${aws_ecr_repository.orchestrator-ecr.repository_url}:latest"
  package_type  = "Image"
  role          = aws_iam_role.iam-lambda-orchestrator.arn
  timeout       = 30
}
