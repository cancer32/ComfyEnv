import re
import subprocess
import urllib.request
import urllib.error


def get_cuda_version():
    try:
        result = subprocess.check_output(["nvidia-smi"]).decode()
        match = re.search(r"CUDA Version:\s+(\d+\.\d+)", result)
        return match.group(1) if match else None
    except (subprocess.CalledProcessError, FileNotFoundError):
        return


def get_pytorch_cuda(min_major=11, min_minor=1):
    """
    Given a CUDA version like '12.7', check decreasing minor versions
    to find a working PyTorch CUDA wheel index using urllib.
    """
    cuda_version = get_cuda_version()
    if not cuda_version:
        print("No supported CUDA version found in PyTorch index. using cpu",
              flush=True)
        return 'cpu'

    try:
        major, minor = map(int, cuda_version.split('.'))
    except ValueError:
        raise ValueError(
            "Invalid CUDA version format. Expected format: '12.7'")

    while (major > min_major) or (major == min_major and minor >= min_minor):
        cuda_tag = f"{major}{minor}"
        url = f"https://download.pytorch.org/whl/cu{cuda_tag}"
        print(f"Checking: {url}", flush=True)
        try:
            with urllib.request.urlopen(url, timeout=5) as response:
                if response.status == 200:
                    print(f"Found: {url}")
                    return f"cu{cuda_tag}"
        except urllib.error.HTTPError as e:
            if e.code == 403:
                print(f"Forbidden (403): {url}", flush=True)
            elif e.code == 404:
                print(f"Not Found (404): {url}", flush=True)
            else:
                print(f"HTTP Error {e.code}: {url}", flush=True)
        except urllib.error.URLError as e:
            print(f"URL Error: {e.reason} at {url}", flush=True)
        except Exception as e:
            print(f"Unknown error: {e}", flush=True)

        # Lower the minor version
        minor -= 1
        if minor < 0:
            major -= 1
            minor = 9  # assume fallback limit

    print("No supported CUDA version found in PyTorch index. using cpu",
          flush=True)
    return "cpu"
