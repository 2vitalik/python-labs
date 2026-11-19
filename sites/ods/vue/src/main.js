import { useMd } from '@core/md.js'
import { start } from '@core/start.js'

import math from './math.js'
import richMd from './richMd.js'
import router from './router.js'
import site from './site.js'
import slideMd from './slideMd.js'
import './style.css'

useMd(math, richMd, slideMd)  // slideMd last: marked asks the last one first
start(site, router)
