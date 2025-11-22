export async function withRetry(fn, retries = 5, wait = 5000) {
  const delay = (ms) => new Promise(res => setTimeout(res, ms));

  for (let attempt = 1; attempt <= retries; attempt++) {
    try {
      return await fn();
    } catch (err) {
      if (attempt === retries) throw err;
      await delay(wait);
    }
  }
}