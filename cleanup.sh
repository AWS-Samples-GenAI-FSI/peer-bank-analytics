#!/bin/bash

STACK_NAME=${1:-banking-analytics}

echo "🧹 Cleaning up Banking Analytics resources..."
echo "📋 Stack name: $STACK_NAME"

# Delete the main stack
echo "Deleting CloudFormation stack..."
aws cloudformation delete-stack --stack-name $STACK_NAME

echo "✅ Cleanup initiated!"
echo "💡 Stack deletion takes 2-3 minutes"
echo "🔍 Check AWS Console > CloudFormation to monitor progress"