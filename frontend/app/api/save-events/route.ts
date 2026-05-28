import { writeFile } from "fs/promises";

export async function POST( 
  req: Request 
) { 
  const events = await req.json(); 
  
  await writeFile( "events.json", JSON.stringify(events, null, 2) ); 
  
  return Response.json({ success: true, }); 
}