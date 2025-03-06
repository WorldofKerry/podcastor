from podcaster_kerry.to_audio import create_piper_json

def test_create_piper_json():
    SAMPLE = """
    H1: Hey, have you read that paper about the Tensor Processing Unit (TPU) from Google? It’s pretty fascinating how they’ve designed a custom ASIC specifically for neural network inference.  
    H2: Yeah, I did! It’s impressive how they managed to deploy it in their datacenters by 2015, just 15 months after starting the project. The TPU seems to be a game-changer for inference workloads.  

    H1: Absolutely. The heart of the TPU is this massive 65,536 8-bit MAC matrix multiply unit, which gives it a peak throughput of 92 TeraOps per second. That’s insane!  
    H2: Right? And they’ve got this 28 MiB software-managed on-chip memory. What’s interesting is how they’ve optimized for deterministic execution, which is crucial for meeting the 99th-percentile response-time requirements of their applications.  
    """
    result = create_piper_json(SAMPLE)
    json_str = "\n".join(json.dumps(r) for r in result)
    print(json_str)

    assert False