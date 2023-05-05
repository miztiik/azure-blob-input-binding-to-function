import logging
import json
import datetime

import azure.functions as func

def main(req: func.HttpRequest, miztProc: func.InputStream, outputBlob: func.Out[str], context: func.Context) -> func.HttpResponse:
# def main(miztProc: func.InputStream, context: func.Context):
    get_req_body = None
    body_blob_name = None
    recv_blob_name = None
    try:
        query_blob_name = req.params.get("blob_name") # For query string
        # For blob_name in body
        get_req_body = req.get_json()
        body_blob_name = get_req_body.get("blob_name")

        if query_blob_name:
            recv_blob_name = query_blob_name
        elif body_blob_name:
            recv_blob_name = body_blob_name

        logging.info(f" Received Blob Name: {recv_blob_name}")
        _d = miztProc.read().decode("utf-8")
        _d = json.loads(_d)
        _d["miztiik_event_processed"] = True
        _d["last_processed_on"] = datetime.datetime.now().isoformat()
        logging.info(f"BLOB DATA: {json.dumps(_d)}")
        outputBlob.set(str(_d)) # Imperative to type cast to str
        logging.info(f"Uploaded to blob storage")
        logging.info(
            json.dumps({
            'ctx_func_name': context.function_name,
            'ctx_func_dir': context.function_directory,
            'ctx_invocation_id': context.invocation_id,
            'ctx_trace_context_Traceparent': context.trace_context.Traceparent,
            'ctx_trace_context_Tracestate': context.trace_context.Tracestate,
            'ctx_retry_context_RetryCount': context.retry_context.retry_count,
            'ctx_retry_context_MaxRetryCount': context.retry_context.max_retry_count,
        })
        )
    except Exception as e:
        logging.exception(f"ERROR:{str(e)}")

    return func.HttpResponse(f"Blob {recv_blob_name}.json processed", status_code=200)
