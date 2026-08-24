const functions = require("firebase-functions/v1");
const admin = require("firebase-admin");

admin.initializeApp();
const db = admin.database();

const NODE_NAME_RE = /^[A-Za-z0-9_-]{1,64}$/;
const ALLOWED_NODES = new Set(
  (process.env.AROHAN_ALLOWED_NODES || "iot,iotA")
    .split(",")
    .map((value) => value.trim())
    .filter(Boolean),
);

function validNode(nodeId) {
  return typeof nodeId === "string" && NODE_NAME_RE.test(nodeId) && ALLOWED_NODES.has(nodeId);
}

exports.health = functions.https.onRequest((_request, response) => {
  response.status(200).json({
    service: "arohan-functions",
    status: "healthy",
  });
});

exports.onCallingStatus = functions.database
  .ref("ronin/iot_nodes/{nodeId}/status/calling_status")
  .onWrite(async (change, context) => {
    if (!change.after.exists() || change.after.val() !== true) {
      return null;
    }
    if (change.before.exists() && change.before.val() === true) {
      return null;
    }

    const { nodeId } = context.params;
    if (!validNode(nodeId)) {
      functions.logger.warn("Rejected unsupported IoT node", { nodeId });
      return null;
    }

    const eventId = `${context.eventId}-${nodeId}`.replace(/[^A-Za-z0-9_-]/g, "_");
    const eventRef = db.ref(`ronin/alerts/${eventId}`);
    const existing = await eventRef.once("value");
    if (existing.exists()) {
      return null;
    }

    await eventRef.set({
      type: "IOT_CALLING_STATUS",
      nodeId,
      severity: "CRITICAL",
      resolved: false,
      timestamp: admin.database.ServerValue.TIMESTAMP,
      source: "firebase-function",
      eventId,
    });
    return null;
  });
