from sqlalchemy import Column, DateTime, Index, Integer, String, Text, func

from app.database import Base


class RequestLog(Base):
    __tablename__ = "fastapi_request_logs"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    url = Column(String(2048), nullable=False)
    method = Column(String(10), nullable=False)
    query_params = Column(Text, default=None)
    request_body = Column(Text, default=None)
    response_body = Column(Text, default=None)
    status_code = Column(Integer, nullable=False)
    response_time_ms = Column(Integer, nullable=False)
    client_ip = Column(String(45), default=None)
    user_agent = Column(String(512), default=None)
    request_headers = Column(Text, default=None)
    user_id = Column(Integer, default=None)
    trace_id = Column(String(32), default=None)
    created_at = Column(DateTime(timezone=True), server_default=func.now())

    __table_args__ = (
        Index("idx_log_created_at", "created_at"),
        Index("idx_log_user_id", "user_id"),
        Index("idx_log_status_code", "status_code"),
        Index("idx_log_method_url", "method", "url"),
        Index("idx_log_trace_id", "trace_id"),
    )
