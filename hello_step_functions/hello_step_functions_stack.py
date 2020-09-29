import aws_cdk.aws_stepfunctions as sfn
import aws_cdk.aws_stepfunctions_tasks as tasks
from aws_cdk import core, aws_lambda_python


class HelloStepFunctionsStack(core.Stack):
    def __init__(self, scope: core.Construct, id: str, **kwargs) -> None:
        super().__init__(scope, id, **kwargs)

        # The code that defines your stack goes here

        submit_lambda = aws_lambda_python.PythonFunction(
            self,
            'submit-status',
            entry='./lambdas/foo',
            handler='submit_status'
        )

        get_status_lambda = aws_lambda_python.PythonFunction(
            self,
            'get-status',
            entry='./lambdas/foo',
            handler='get_status'
        )

        final_status_lambda = aws_lambda_python.PythonFunction(
            self,
            'final-status',
            entry='./lambdas/foo',
            handler='final_status'
        )

        submit_job = tasks.LambdaInvoke(
            self,
            "Submit Job",
            lambda_function=submit_lambda,
            output_path="$.Payload",
        )

        wait_x = sfn.Wait(
            self, "Wait X Seconds", time=sfn.WaitTime.seconds_path("$.seconds")
        )

        get_status = tasks.LambdaInvoke(
            self,
            "Get Job Status",
            lambda_function=get_status_lambda,
            output_path="$.Payload",
        )

        job_failed = sfn.Fail(
            self,
            "Job Failed",
            cause="AWS Batch Job Failed",
            error="DescribeJob returned FAILED",
        )

        final_status = tasks.LambdaInvoke(
            self,
            "Get Final Job Status",
            lambda_function=final_status_lambda,
            output_path="$.Payload",
        )

        definition = (
            submit_job.next(wait_x)
            .next(get_status)
            .next(
                sfn.Choice(self, "Job Complete?")
                .when(sfn.Condition.string_equals("$.status", "FAILED"), job_failed)
                .when(
                    sfn.Condition.string_equals("$.status", "SUCCEEDED"), final_status
                )
                .otherwise(wait_x)
            )
        )

        sfn.StateMachine(
            self, "StateMachine", definition=definition, timeout=core.Duration.minutes(5)
        )
