import torch

def list_all_devices():
    devices = []

    # CPU is always available
    devices.append(("CPU", "cpu"))

    # Check for CUDA devices
    if torch.cuda.is_available():
        num_cuda_devices = torch.cuda.device_count()
        for i in range(num_cuda_devices):
            devices.append((f"CUDA:{i} - {torch.cuda.get_device_name(i)}", f"cuda:{i}"))

    # Check for MPS (Apple Silicon) devices
    if hasattr(torch.backends, "mps") and torch.backends.mps.is_available():
        devices.append(("MPS", "mps"))

    # List all available devices
    print("Available devices:")
    for name, device in devices:
        print(f"{name} ({device})")

    return devices

available_devices = list_all_devices()

# Example of using MPS if available
if torch.backends.mps.is_available():
    device = torch.device("mps")
    print("Using MPS device")
else:
    device = torch.device("cpu")
    print("Using CPU device")

# Create a tensor on the selected device
tensor = torch.randn((3, 3), device=device)
print(tensor)
