/**
 * AUTO-GENERATED SERVER COMPONENT (BFF)
 * TRUSTWARE CERTIFIED DATA COUPLER
 */

import SynthesizedPageClient from './SynthesizedPage.client';

export default async function Page() {
  let workspaceStatus = null;
  try {
    const res = await fetch(process.env.INTERNAL_API_GATEWAY + '/api/antigravity/v1/workspace', {
      method: 'GET',
      cache: 'no-store',
      headers: {
        'Authorization': `Bearer ${process.env.BFF_INTERNAL_TOKEN}`,
        'X-Aurora-Scope': 'workspace:read'
      }
    });
    if (!res.ok) {
      throw new Error(`BFF Fetch Error: ${res.statusText}`);
    } else {
      workspaceStatus = await res.json();
    }
  } catch (error) {
    throw new Error(`BFF Fetch Error: ${error.message}`);
  }

  return <SynthesizedPageClient workspaceStatus={workspaceStatus} />;
}
