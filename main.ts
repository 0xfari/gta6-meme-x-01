// gta6-meme-x-01 entrypoint. The entry is the post itself, so this program
// only delivers POST.json (the post's address) to the grader's output dir.
import { mkdir, readFile, writeFile } from 'node:fs/promises';
import { join } from 'node:path';

async function deliverPost(): Promise<void> {
  const sourceDir = process.env.MAKEFUN_BOT_DIR ?? '/bot';
  const targetDir = process.env.MAKEFUN_OUTPUT_DIR ?? '/output';
  await mkdir(targetDir, { recursive: true });
  const payload = await readFile(join(sourceDir, 'POST.json'));
  await writeFile(join(targetDir, 'POST.json'), payload);
}

deliverPost().catch((err: unknown) => {
  console.error(`POST.json could not be delivered: ${(err as Error).message}`);
  process.exit(1);
});
