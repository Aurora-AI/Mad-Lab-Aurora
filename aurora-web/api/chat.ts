import type { VercelRequest, VercelResponse } from '@vercel/node';

export default async function handler(req: VercelRequest, res: VercelResponse) {
  if (req.method !== 'POST') {
    return res.status(405).json({ error: 'Method not allowed' });
  }

  const apiKey = process.env.GEMINI_API_KEY;
  if (!apiKey) {
    return res.status(500).json({ error: 'Service unavailable' });
  }

  const { message, history, systemInstruction } = req.body ?? {};
  if (!message) {
    return res.status(400).json({ error: 'message required' });
  }

  try {
    const { GoogleGenAI } = await import('@google/genai');
    const ai = new GoogleGenAI({ apiKey });

    const chat = ai.chats.create({
      model: 'gemini-2.0-flash',
      config: { systemInstruction },
      history: history ?? [],
    });

    const response = await chat.sendMessage({ message });
    return res.status(200).json({ text: response.text });
  } catch (err: unknown) {
    const message = err instanceof Error ? err.message : 'upstream error';
    return res.status(502).json({ error: message });
  }
}
