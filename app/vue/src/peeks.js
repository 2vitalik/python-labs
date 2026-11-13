import { registerPeeks } from '@core/peek.js'

import PeekEntity from './components/PeekEntity.vue'
import PeekRule from './components/PeekRule.vue'
import PeekTask from './components/PeekTask.vue'
import PeekWindow from './components/PeekWindow.vue'

// what the cards under the mouse show on this site (T284 §2): v-peek="{ kind, id }", id — a part's or a rule's id, a card's slug
registerPeeks({ window: PeekWindow, entity: PeekEntity, rule: PeekRule, task: PeekTask })
