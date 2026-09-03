import json
import re

log_path = r'C:\Users\graha\.gemini\antigravity-ide\brain\01eebd44-ac12-4e1c-a04d-123a796db15b\.system_generated\logs\transcript.jsonl'
output_path = r'CONVERSATION_LOG.md'

user_messages = []
assistant_summaries = []

with open(log_path, encoding='utf-8') as f:
    for line in f:
        if not line.strip():
            continue
        try:
            entry = json.loads(line)
            entry_type = entry.get('type')
            content = entry.get('content', '')
            
            # Capture User Inputs
            if entry_type == 'USER_INPUT' and content:
                # Strip out system metadata wrapper if present
                clean_content = content
                if '<USER_REQUEST>' in clean_content:
                    match = re.search(r'<USER_REQUEST>\s*(.*?)\s*</USER_REQUEST>', clean_content, re.DOTALL)
                    if match:
                        clean_content = match.group(1).strip()
                
                # Exclude internal system messages
                if not clean_content.startswith('<SYSTEM_MESSAGE>') and not clean_content.startswith('Here are the'):
                    user_messages.append(clean_content)

            # Capture Planner/Model Responses
            elif entry_type == 'PLANNER_RESPONSE' and content:
                if not content.startswith('<thought>'):
                    assistant_summaries.append(content.strip())
        except Exception:
            pass

# Format into Markdown
md = []
md.append("# CoverStar Kids Parties - Project Conversation Log & Trajectory\n")
md.append("This document contains the complete record of user requests, decisions, design adjustments, and technical enhancements made during the development of **CoverStar Kids Parties Liverpool**.\n")
md.append("---\n")

md.append("## Executive Summary of Key Milestones\n")
md.append("1. **Dual Design Concepts Built**: Created High-Energy Fun Style (Option A on `index.html`) and Classic Style (Option B on `classic-version.html`).")
md.append("2. **Slow Ambient Background Scroll**: Adjusted continuous horizontal marquee animation duration to 75 seconds for gentle, smooth motion.")
md.append("3. **Find Us & Opening Hours**: Added Prohibition Recording Studios address (24 Arrad Street, L1 3BP), opening hours, phone (`0800 689 7827`), transport info, and interactive Google Maps embed.")
md.append("4. **Authentic TripAdvisor Award Badge**: Downloaded and masked the official green TripAdvisor Travellers' Choice Award seal without the 2025 date text into a clean 1:1 round badge.")
md.append("5. **SEO Target Keyword Optimization**: Applied target keyword `Kids Parties Liverpool` to Meta Title (`Kids Parties Liverpool | 10-Time TripAdvisor Winners`) and Meta Description.")
md.append("6. **Sitewide Header & Footer Standardization**: Standardized top bar, navigation menu, and 3-column footer with logo across all 9 pages (`index.html`, `classic-version.html`, `about-coverstar`, `contact`, `legal/privacy-policy`, `terms-and-conditions`, `cookie-policy`, `accessibility`, `404.html`).")
md.append("7. **Mobile-First Responsive Ergonomics**: Fixed mobile header nav drawer, enlarged mobile brand logo (`48px`), matched mobile sticky bottom CTA buttons to hero buttons, and isolated mobile hero element order without affecting 2-column desktop grid.\n")
md.append("---\n")

md.append("## Detailed Chronological Transcript\n")

# Combine messages chronologically
idx = 1
for user_msg in user_messages:
    md.append(f"### Request {idx}\n")
    md.append(f"**User:**\n> {user_msg}\n")
    idx += 1

with open(output_path, 'w', encoding='utf-8') as out:
    out.write('\n'.join(md))

print(f'Successfully exported conversation log to {output_path}!')
