import kagglehub

# Download latest version
path = kagglehub.dataset_download("prasad22/daily-transactions-dataset")

print("Path to dataset files:", path)