import logging

from pegasus_xsum import PegasusXSum as Model
from simple_ai.api.grpc.completion.server import LanguageModelServicer, serve
import torch
# reduce the default memory reserved by PyTorch


if __name__ == "__main__":
    import argparse

    logging.basicConfig(level=logging.INFO)

    parser = argparse.ArgumentParser()
    parser.add_argument("-a", "--address", type=str, default="[::]:50051")
    args = parser.parse_args()

    logging.info(f"Starting gRPC server on {args.address}")

    model_servicer = LanguageModelServicer(model=Model())
    serve(address=args.address, model_servicer=model_servicer)