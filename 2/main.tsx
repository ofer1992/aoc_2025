import fs from 'fs';

const input = fs.readFileSync("2/input.txt", 'utf-8');
// const input = "11-22,95-115,998-1012,1188511880-1188511890,222220-222224,1698522-1698528,446443-446449,38593856-38593862,565653-565659,824824821-824824827,2121212118-2121212124"

function process(input: string): number[][] {
    return input.split(",")
        .map(t => t.split('-'))
        .map(([a, b]) => [parseInt(a), parseInt(b)]);
}

function one(input: string) {
    const ranges = process(input);
    // Looking for all invalid ids in range. An invalid id is a number of the form xx.

    let c = 0;
    ranges.forEach(([a, b]) => {
        console.log(a, b);
        for (let i = a; i <= b; i++) {
            const iStr = i.toString();
            const len = iStr.length;
            if (len % 2 === 1) continue;
            // console.log(iStr.slice(0, len / 2), iStr.slice(len / 2, len));
            if (iStr.slice(0, len / 2) === iStr.slice(len / 2, len)) {
                console.log(i);
                c += i;
            }
        }
    });
    return c
}

function isPeriodic(n: number) {
    const s = n.toString();
    for (let p = 1; p <= s.length / 2; p++) {
        if (s.length % p != 0) continue;
        let violated = false;
        for (let i = 0; i < s.length - p; i++) {
            if (s[i] != s[i + p]) {
                violated = true;
                break;
            }
        }
        if (!violated) return true;
    }
    return false;

}

// part two - naive approach
function two(input: string) {
    const ranges = process(input);
    let c = 0;
    ranges.forEach(([a, b]) => {
        // console.log(a, b);
        for (let i = a; i <= b; i++) {
            if (isPeriodic(i)) {
                // console.log(i);
                c += i;
            }
        }
    });
    return c
}
