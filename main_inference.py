from data_model_inference.model_inference import ModelInference



def main():
    inference = ModelInference(None, 30)
    inference.start_streaming()
    while True:
        inference.stream_loop()


if __name__ == "__main__":
    main()