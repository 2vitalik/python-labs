// which emoji this device draws (T309; the way emoji-picker-element tells): an emoji painted black and painted white is
// the same picture only when the font has it in colour — a missing one comes as a box in the ink's colour. One emoji is
// asked per Unicode Emoji version, the newest first: the picker hides what came later than the device knows
const TESTS = [[18, '🫫'], [17, '🫪'], [16, '🫩'], [15, '🫨'], [14, '🫠'], [13, '🥲'], [12, '🥱'], [11, '🥰'], [5, '🤩']]
const FONT = '100px "Apple Color Emoji","Segoe UI Emoji","Noto Color Emoji","Twemoji Mozilla",sans-serif'
let ctx, max

function paint(char, ink) {
  ctx.clearRect(0, 0, 100, 100)
  ctx.fillStyle = ink
  ctx.fillText(char, 0, 0)
  return ctx.getImageData(0, 0, 1, 1).data.join()
}
export function draws(char) {
  if (!ctx) {
    const canvas = Object.assign(document.createElement('canvas'), { width: 1, height: 1 })
    ctx = canvas.getContext('2d', { willReadFrequently: true })
    Object.assign(ctx, { textBaseline: 'top', font: FONT })
    ctx.scale(0.01, 0.01)  // the whole glyph into one pixel
  }
  const black = paint(char, '#000')
  return black === paint(char, '#fff') && !black.startsWith('0,0,0,')
}
export const maxVersion = () => (max ??= TESTS.find(([, char]) => draws(char))?.[0] || 4)
