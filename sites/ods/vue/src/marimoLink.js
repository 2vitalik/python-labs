import lz from 'lz-string'

// marimo's playground runs a notebook in the visitor's own browser (Pyodide); the code rides after `#`, which browsers never send to a server
export const marimoLink = (code) => `https://marimo.app/#code/${lz.compressToEncodedURIComponent(code)}`
