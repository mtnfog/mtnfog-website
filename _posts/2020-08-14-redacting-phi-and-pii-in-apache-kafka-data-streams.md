---
date: 2020-08-21
title: Redacting PHI and PII from Apache Kafka Data Streams
layout: post
categories:
  - philter
  - java
redirect_from: /phirestream/redacting-phi-and-pii-in-apache-kafka-streaming-pipelines/
---

Apache Kafka can be found in virtually every industry today. Its ability to scale and efficiently process streaming data has made it a cornerstone of data streaming architectures. Some industries, like healthcare  may have restrictions on the data being processed. HIPAA has rules around how PHI (Protected Health Information) is handled.

If you are ingesting streaming patient data you may need to redact sensitive information, like patient names and birthdates, in the text. Redacting sensitive information from the streaming data can help protect a pipeline against inadvertent exposure of PHI and PII and it could help get the data into a format so it can be used for secondary purposes, such as training a machine learning model.

# Phirestream

<img src="/images/phirestream-logo-transparent.png">

<a href="/phirestream">Phirestream</a> works alongside Apache Kafka to redact PHI and PII in data streams. Phirestream provides an implementation of Apache Kafka’s REST interface that receives your data, redacts the sensitive information, and then sends the redacted data to its destination Apache Kafka topic. It doesn’t require you to modify your data ingest pipelines. Instead, you can simply “inject” Phirestream into your pipeline with minimal configuration changes.

You can configure Phirestream to redact the types of PHI and PII you need, such as person’s names, ages, dates, zip codes, and more. You can choose to simply redact each instance of PHI and PII or you can encrypt, anonymize, or randomize the values. Phirestream gives you complete control over how your streaming data is to be redacted.

## Using Phirestream

Here’s how to use Phirestream. In the example curl request below we are sending a small piece of text to Phirestream for redaction.

```
curl -k -X POST \
    https://localhost:8080/topics/default \
    -H 'Content-Type: application/vnd.kafka.json.v2+json' \
    -d '{
        "records": [
            {
                "key": "key-1",
                "value": "George Washington was president.",
                "headers": [
                    {"key": "profile", "value": "default"}
                ]
            },
        ]
    }'
```

Phirestream receives the text, redacts the person’s name (George Washington) and then publishes the redacted text to an Apache Kafka topic named default. To see the redacted text we can consume from the topic:

```
kafka-console-consumer.sh \
    --topic default \
    --bootstrap-server localhost:9092 \
    --from-beginning
```

The output of this command will be the redacted text:

```
{% raw %}
{{{REDACTED-entity}}} was president.
{% endraw %}
```

## Filter Profiles

The types of sensitive information that are identified by Phirestream are defined in files called filter profiles. A filter profile specifies the types of sensitive information and how to redact those types. Phirestream selects which filter profile to apply based on the name of the Apache Kafka topic. In the example above, the topic name was default so the filter profile named default was applied. Learn more about filter profiles.