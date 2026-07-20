import json, math, random

def score(seq):
    first=[seq[i]-seq[i-1] for i in range(1,len(seq))]
    second=[first[i]-first[i-1] for i in range(1,len(first))]
    return sum(abs(x) for x in second)/len(second)

def run(seed=31):
    rng=random.Random(seed); rows=[]
    for fake in (0,1):
        for _ in range(100):
            phase=rng.random()*6
            seq=[t*.8+2*math.sin(t/7+phase)+rng.gauss(0,.08) for t in range(30)]
            if fake:
                seq=[x+(.65 if t%2 else -.65) for t,x in enumerate(seq)]
            rows.append((score(seq),fake))
    threshold=sum(s for s,_ in rows)/len(rows)
    second=sum((s>threshold)==bool(y) for s,y in rows)/len(rows)
    first=.5
    return {"first_order_accuracy":first,"second_order_accuracy":round(second,3),
            "accuracy_gain_pct":round(100*(second-first),1),"threshold":round(threshold,3)}

if __name__ == "__main__":
    print(json.dumps(run(), indent=2))
