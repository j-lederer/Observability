def update_trace_context(header):
    # Parse incoming header
    traceparent = header.get("traceparent", "")
    tracestate = header.get("tracestate", "")

    if traceparent:
        # Parse traceparent
        version, trace_id, parent_id, flags = traceparent.split("-")

        # Update tracestate with DataCat information
        tracestate_entries = tracestate.split(",") if tracestate else []
        tracestate_entries.append("dc=.2")

        # Construct outgoing header
        outgoing_header = {
            "traceparent": f"{version}-{trace_id}-{parent_id}-{flags}",
            "tracestate": ",".join(tracestate_entries)
        }

        return outgoing_header

    return header

# Test inputs
test_inputs = [
    {"traceparent": "00-0af7651916cd43dd8448eb211c80319c-b9c7c989f97918e1-01",
     "tracestate": "congo=ucfJifl5GOE,rojo=00f067aa0ba902b7"},
    {"traceparent": "00-0af7651916cd43dd8448eb211c80319c-b9c7c989f97918e1-01",
     "tracestate": "dc=.2,congo=ucfJifl5GOE"},
    {"traceparent": "00-0af7651916cd43dd8448eb211c80319c-b9c7c989f97918e1-01",
     "tracestate": "congo=ucfJifl5GOE,dc=1"},
    {"tracestate": "congo=ucfJifl5GOE,dc=1"},
    {"traceparent": "00-0af7651916cd43dd8448eb211c80319c-b9c7c989f97918e1-01"},
    {}
]

# Test the function for each input and print the result
for i, input_data in enumerate(test_inputs, start=1):
    result = update_trace_context(input_data)
    print(f"{i}. {result}")