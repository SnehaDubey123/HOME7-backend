import base64
import json
import logging
import os

from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_POST
from openai import OpenAI

logger = logging.getLogger(__name__)


def _clean_text(value, default='Not specified', max_length=200):
    if value is None:
        return default
    return str(value).strip()[:max_length] or default


@csrf_exempt
@require_POST
def generate_floorplan(request):
    """Accept HOME7 design preferences and return a base64 PNG image."""
    api_key = os.getenv('OPENAI_API_KEY', '').strip()
    if not api_key or api_key == 'replace_with_your_real_api_key':
        return JsonResponse(
            {'error': 'OPENAI_API_KEY is missing. Add your key to backend/.env and restart Django.'},
            status=500,
        )

    try:
        payload = json.loads(request.body.decode('utf-8'))
    except (json.JSONDecodeError, UnicodeDecodeError):
        return JsonResponse({'error': 'Request body must be valid JSON.'}, status=400)

    if not isinstance(payload, dict):
        return JsonResponse({'error': 'Request body must be a JSON object.'}, status=400)

    try:
        width = float(payload.get('width', 0))
        length = float(payload.get('length', 0))
    except (TypeError, ValueError):
        return JsonResponse({'error': 'Width and length must be numeric.'}, status=400)

    if not (0 < width <= 500 and 0 < length <= 500):
        return JsonResponse({'error': 'Width and length must be greater than 0 and no more than 500 feet.'}, status=400)

    home_type = _clean_text(payload.get('home_type'), '1BHK')
    direction = _clean_text(payload.get('direction'))
    style = _clean_text(payload.get('style'))
    budget = _clean_text(payload.get('budget'))
    spaces = payload.get('spaces', [])
    furniture = payload.get('furniture', [])
    if not isinstance(spaces, list):
        spaces = []
    if not isinstance(furniture, list):
        furniture = []
    spaces_text = ', '.join(_clean_text(x, max_length=100) for x in spaces[:30]) or 'No additional spaces selected'
    furniture_text = ', '.join(_clean_text(x, max_length=100) for x in furniture[:50]) or 'No furniture preferences specified'

    prompt = f'''Create a clear, professional ARCHITECTURAL 2D TOP-DOWN FLOOR PLAN CONCEPT for a residential home.

Home type: {home_type}
Outer dimensions: {width:g} feet wide by {length:g} feet long (approximately {width * length:g} square feet).
Entrance direction: {direction}
Interior style: {style}
Budget range: {budget}
Required additional spaces: {spaces_text}
Requested furniture: {furniture_text}

Visual requirements:
- Show a top-down orthographic floor plan, not a perspective room render and not an exterior building image.
- Draw clear walls, door openings with swing arcs, windows, room boundaries and sensible circulation.
- Label rooms legibly in English; include approximate room dimensions where possible.
- Arrange furniture at realistic scale and do not block doors or main walkways.
- Respect the overall footprint and fit the requested spaces logically. If every preference cannot fit, prioritize safe circulation and essential rooms.
- Use a clean white background, precise dark architectural lines, restrained subtle colors, and a neat professional presentation.
- Avoid decorative text, watermarks, logos, people, and misleading structural engineering details.
- This is an AI concept only, not a permit-ready or construction-certified drawing.
'''

    try:
        client = OpenAI(api_key=api_key)
        result = client.images.generate(
            model='gpt-image-2',
            prompt=prompt,
            size='1024x1024',
        )
        image_b64 = result.data[0].b64_json
        if not image_b64:
            return JsonResponse({'error': 'The image service returned no image data.'}, status=502)
        # This is the response format main.dart already handles.
        return JsonResponse({'image_base64': image_b64, 'mime_type': 'image/png'})
    except Exception as exc:
        logger.exception('HOME7 floor plan generation failed')
        # Return a useful message without exposing credentials or full internal traces.
        message = str(exc)
        if '401' in message or 'authentication' in message.lower() or 'api key' in message.lower():
            message = 'OpenAI authentication failed. Check OPENAI_API_KEY in backend/.env.'
        elif '429' in message or 'quota' in message.lower() or 'billing' in message.lower():
            message = 'OpenAI quota or rate limit reached. Check your API account billing and limits.'
        else:
            message = 'Image generation failed. Check the Django terminal for details.'
        return JsonResponse({'error': message}, status=502)
