I apologize for misunderstanding your request earlier. I see now that you're looking for the complete code encapsulated within a GitHub-style README. Here's how that would look:

---

# MuleSoft Application with Azure Application Insights Integration

This repository demonstrates how to integrate Azure Application Insights into a MuleSoft application for telemetry gathering.

## Prerequisites

- An active Azure subscription.
- An Application Insights resource created in Azure.
- Mule 4 runtime and Anypoint Studio.

## Getting Started

### Step 1: Add Application Insights SDK Dependency

Modify your Mule project's `pom.xml`:

```xml
<dependency>
    <groupId>com.microsoft.azure</groupId>
    <artifactId>applicationinsights-core</artifactId>
    <version>2.6.2</version> <!-- Check for the latest version -->
</dependency>
```

### Step 2: Configuration

Add a `global.xml` file to your Mule project:

```xml
<?xml version="1.0" encoding="UTF-8"?>

<mule xmlns="http://www.mulesoft.org/schema/mule/core"
      xmlns:doc="http://www.mulesoft.org/schema/mule/documentation"
      xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance"
      xsi:schemaLocation="http://www.mulesoft.org/schema/mule/core http://www.mulesoft.org/schema/mule/core/current/mule.xsd">
       
    <configuration-properties file="application-insights-config.properties" doc:name="Configuration properties" />

</mule>
```

Next, add an `application-insights-config.properties` to your Mule project's `src/main/resources` directory:

```
app.insights.key=YOUR_INSTRUMENTATION_KEY
```

### Step 3: Application Instrumentation

Here's a sample flow:

```xml
<flow name="instrumentedFlow">
    <http:listener doc:name="Listener" config-ref="HTTP_Listener_config" path="/test"/>
    <set-payload value="Test Response" doc:name="Set Payload"/>
    <component doc:name="Send Telemetry">
        <scripting:script engine="groovy">
            <![CDATA[
                import com.microsoft.applicationinsights.TelemetryClient;

                TelemetryClient telemetry = new TelemetryClient();
                telemetry.getContext().setInstrumentationKey(app.insights.key);
                telemetry.trackEvent("ReceivedRequestOnInstrumentedFlow");
                return payload;
            ]]>
        </scripting:script>
    </component>
</flow>
```

### Step 4: Deployment

1. Deploy the instrumented Mule application.
2. Send a request to the flow (e.g., `http://localhost:8081/test`).
3. Check the Azure Application Insights portal to confirm telemetry data reception.

## Documentation

For more details, consult:

- [Azure Application Insights](https://docs.microsoft.com/en-us/azure/azure-monitor/app/app-insights-overview)
- [Application Insights Java SDK on GitHub](https://github.com/microsoft/ApplicationInsights-Java)
- [MuleSoft Documentation](https://docs.mulesoft.com/mule-runtime/4.3/)

## License

This project is under the MIT License - see the [LICENSE.md](LICENSE.md) file for details.

---

Ensure to replace placeholders such as `YOUR_INSTRUMENTATION_KEY` with actual values.
