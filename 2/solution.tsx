import fs from 'fs';

const input = fs.readFileSync("2/input.txt", 'utf-8');

function process(input: string): number[][] {
    return input.split(",")
        .map(t => t.split('-'))
        .map(([a, b]) => [parseInt(a), parseInt(b)]);
}

function isPeriodic(n: number): boolean {
    const s = n.toString();
    for (let p = 1; p <= s.length / 2; p++) {
        if (s.length % p !== 0) continue;
        let valid = true;
        for (let i = 0; i < s.length - p; i++) {
            if (s[i] !== s[i + p]) {
                valid = false;
                break;
            }
        }
        if (valid) return true;
    }
    return false;
}

// Generate periodic number from pattern and repetitions
function makePeriodicNumber(pattern: string, reps: number): number {
    return parseInt(pattern.repeat(reps));
}

// Find first periodic number of given length
function firstPeriodicOfLength(len: number): number {
    // Find LARGEST period that divides len (gives smallest number)
    for (let period = Math.floor(len / 2); period >= 1; period--) {
        if (len % period === 0) {
            const pattern = '1' + '0'.repeat(period - 1);
            return makePeriodicNumber(pattern, len / period);
        }
    }
    return -1;
}

// Find next periodic number after n
function nextPeriodic(n: number): number {
    const s = n.toString();
    const len = s.length;
    const candidates: number[] = [];

    // Case 1: Next length (always the minimal periodic of that length)
    candidates.push(firstPeriodicOfLength(len + 1));

    // Case 2: Same length - try all possible periods
    for (let period = 1; period <= len / 2; period++) {
        if (len % period !== 0) continue;
        const reps = len / period;

        const pattern = s.slice(0, period);
        const patternNum = parseInt(pattern);

        // Try current pattern
        const samePattern = makePeriodicNumber(pattern, reps);
        if (samePattern > n) {
            candidates.push(samePattern);
        }

        // Try pattern + 1 (if it doesn't overflow)
        const nextPattern = (patternNum + 1).toString();
        if (nextPattern.length === period) {
            const nextCandidate = makePeriodicNumber(nextPattern, reps);
            if (nextCandidate > n) {
                candidates.push(nextCandidate);
            }
        }
    }

    return Math.min(...candidates.filter(c => !isNaN(c)));
}

// Optimized version
function twoOptimized(input: string) {
    const ranges = process(input);
    let sum = 0;

    ranges.forEach(([a, b]) => {
        // Start at a if it's periodic, otherwise find next periodic after a
        let current = isPeriodic(a) ? a : nextPeriodic(a);
        while (current <= b) {
            sum += current;
            current = nextPeriodic(current);
        }
    });

    return sum;
}

// Brute force for comparison
function twoBruteForce(input: string) {
    const ranges = process(input);
    let sum = 0;
    ranges.forEach(([a, b]) => {
        for (let i = a; i <= b; i++) {
            if (isPeriodic(i)) {
                sum += i;
            }
        }
    });
    return sum;
}

// Test
console.log("Testing on full input:\n");

const start1 = performance.now();
const result1 = twoBruteForce(input);
const time1 = performance.now() - start1;

console.log("Brute Force:");
console.log(`  Result: ${result1}`);
console.log(`  Time: ${time1.toFixed(2)}ms\n`);

const start2 = performance.now();
const result2 = twoOptimized(input);
const time2 = performance.now() - start2;

console.log("Optimized (nextPeriodic v2):");
console.log(`  Result: ${result2}`);
console.log(`  Time: ${time2.toFixed(2)}ms\n`);

console.log("Comparison:");
console.log(`  Results match: ${result1 === result2}`);
if (result1 === result2) {
    console.log(`  Speedup: ${(time1 / time2).toFixed(2)}x faster`);
}
