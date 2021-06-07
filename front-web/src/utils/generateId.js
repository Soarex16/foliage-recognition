/**
 * Helper function for generating pseudo random Id
 * Not as good as UUID, but good enough for simple cases
 * @return {string} - generated id
 */
export default function generateId() {
    return Math.trunc(Math.random() * 10e16).toString(32);
}
