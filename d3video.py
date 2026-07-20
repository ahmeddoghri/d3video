import json, math, random

def first_order_score(seq):
    d = [seq[i]-seq[i-1] for i in range(1,len(seq))]
    return sum(abs(x) for x in d)/len(d)

def second_order_score(seq):
    first = [seq[i]-seq[i-1] for i in range(1,len(seq))]
    second = [first[i]-first[i-1] for i in range(1,len(first))]
    return sum(abs(x) for x in second)/len(second)

def accuracy(scored):
    threshold = sum(s for s,_ in scored)/len(scored)
    acc = sum((s>threshold)==bool(y) for s,y in scored)/len(scored)
    return acc, threshold

def run(seed=31):
    rng=random.Random(seed); sequences=[]
    for fake in (0,1):
        for _ in range(100):
            phase=rng.random()*6
            seq=[t*.8+2*math.sin(t/7+phase)+rng.gauss(0,.08) for t in range(30)]
            if fake:
                seq=[x+(.15 if t%2 else -.15) for t,x in enumerate(seq)]
            sequences.append((seq,fake))
    first, _ = accuracy([(first_order_score(s), y) for s,y in sequences])
    second, threshold = accuracy([(second_order_score(s), y) for s,y in sequences])
    return {"first_order_accuracy":round(first,3),"second_order_accuracy":round(second,3),
            "accuracy_gain_pct":round(100*(second-first),1),"threshold":round(threshold,3)}

if __name__ == "__main__":
    print(json.dumps(run(), indent=2))
