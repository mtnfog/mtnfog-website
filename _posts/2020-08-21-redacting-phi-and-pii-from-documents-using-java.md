---
date: 2020-08-21
title: Redacting PHI and PII from Documents using Java
layout: post
categories:
  - philter
  - java
redirect_from: /blog/redacting-phi-and-pii-from-documents-using-java/
---

When you need to redact sensitive information like Protected Health Information (PHI) and Personally Identifiable Information (PII) from documents the Philter SDK for Java has you covered!

The <a href="https://github.com/mtnfog/philter-sdk-java">Philter SDK for Java</a> is an open source project that provides a client SDK for <a href="/philter">Philter</a>. With this library it is easy to redact PHI and PII from documents using Philter. Here’s an example:

In our Maven project we will add the dependency:

```
<dependency>
  <groupId>com.mtnfog</groupId>
  <artifactId>philter-sdk-java</artifactId>
  <version>1.3.0</version>
</dependency>
```

Now, we can instantiate a client:

```
PhilterClient client = new PhilterClient.PhilterClientBuilder().withEndpoint("https://127.0.0.1:8080").build();
FilterResponse filterResponse = client.filter(text);
```

Be sure to change the endpoint to the endpoint of your running Philter instance. Now you are ready to redact!

```
FilterResponse response = client.filter("George Washington was president.");
```

The text parameter will be sent to Philter for redaction. The returned object will contain a value that is the redacted text. With the default settings, that return value will be <code>{% raw %}{{{REDACTED-ner}}}{% endraw %}</code> was president.

If you want to get more details of what happened you can use the explain function instead.

```
ExplainResponse response = client.explain("George Washington was president.");
```

The explain function provides insight into what Philter redacted and why it was redacted. You can use explain to help tune your redaction or for troubleshooting.

That’s it! Now you are ready to integrate Philter’s powerful redaction capabilities into your Java libraries and applications. For full samples check out the project’s <a href="https://github.com/mtnfog/philter-sdk-java/blob/master/src/test/java/com/mtnfog/test/philter/PhilterClientTest.java">test class</a>.

The Philter SDK for Java is licensed under the Apache License, version 2. It is available on <a href="https://github.com/mtnfog/philter-sdk-java">GitHub</a>.