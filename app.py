#!/usr/bin/env python3

from aws_cdk import core

from hello_step_functions.hello_step_functions_stack import HelloStepFunctionsStack


app = core.App()
HelloStepFunctionsStack(app, "hello-step-functions")

app.synth()
