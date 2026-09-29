import { useMd } from '@core/md.js'
import { start } from '@core/start.js'

import math from './math.js'
import router from './router.js'
import site from './site.js'
import './style.css'

useMd(math)
start(site, router)
