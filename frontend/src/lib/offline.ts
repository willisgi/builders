import { openDB } from 'idb'

const DB_NAME = 'kenyapos'
const DB_VERSION = 1

export async function getDb() {
  return openDB(DB_NAME, DB_VERSION, {
    upgrade(db) {
      if (!db.objectStoreNames.contains('offline-sales')) {
        db.createObjectStore('offline-sales', { keyPath: 'id', autoIncrement: true })
      }
    }
  })
}

export async function enqueueOfflineSale(sale: any) {
  const db = await getDb()
  await db.add('offline-sales', { ...sale, createdAt: Date.now() })
}

export async function flushOfflineSales(sender: (sale: any) => Promise<any>) {
  const db = await getDb()
  const tx = db.transaction('offline-sales', 'readwrite')
  const store = tx.objectStore('offline-sales')
  let cursor = await store.openCursor()
  while (cursor) {
    const sale = cursor.value
    try {
      await sender(sale)
      await store.delete(cursor.key as IDBValidKey)
    } catch (_) {
      // keep in queue if failed
    }
    cursor = await cursor.continue()
  }
  await tx.done
}
