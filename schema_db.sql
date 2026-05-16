-- ============================================================
--  SISTEMA DE RESERVAS - DISCOTECA
--  Base de datos PostgreSQL para Supabase
--  Sin integración Telegram | Sin pasarela de pagos
--  Versión: 1.0
-- ============================================================

-- ============================================================
--  SCHEMAS
-- ============================================================
CREATE SCHEMA IF NOT EXISTS catalog;
CREATE SCHEMA IF NOT EXISTS core;
CREATE SCHEMA IF NOT EXISTS transactions;
CREATE SCHEMA IF NOT EXISTS audit;
CREATE SCHEMA IF NOT EXISTS system;


-- ============================================================
--  SCHEMA: catalog
--  Tablas de referencia / catálogos del sistema
-- ============================================================

CREATE TABLE catalog.type_users (
    id   INTEGER      NOT NULL,
    name VARCHAR(100) NOT NULL,
    CONSTRAINT type_users_pkey PRIMARY KEY (id)
);
COMMENT ON TABLE catalog.type_users IS 'Roles de usuario: cliente, admin, staff';

CREATE TABLE catalog.event_states (
    id   INTEGER      NOT NULL,
    name VARCHAR(100) NOT NULL,
    CONSTRAINT event_states_pkey PRIMARY KEY (id)
);
COMMENT ON TABLE catalog.event_states IS 'Estados de un evento: activo, cancelado, finalizado';

CREATE TABLE catalog.reservation_states (
    id   INTEGER      NOT NULL,
    name VARCHAR(100) NOT NULL,
    CONSTRAINT reservation_states_pkey PRIMARY KEY (id)
);
COMMENT ON TABLE catalog.reservation_states IS 'Estados de reserva: pendiente, confirmada, expirada, cancelada';

CREATE TABLE catalog.table_states (
    id   INTEGER      NOT NULL,
    name VARCHAR(100) NOT NULL,
    CONSTRAINT table_states_pkey PRIMARY KEY (id)
);
COMMENT ON TABLE catalog.table_states IS 'Estados de mesa: disponible, reservada, fuera_de_servicio';

CREATE TABLE catalog.table_types (
    id   INTEGER      NOT NULL,
    name VARCHAR(100) NOT NULL,
    CONSTRAINT table_types_pkey PRIMARY KEY (id)
);
COMMENT ON TABLE catalog.table_types IS 'Tipos de mesa: VIP, regular, terraza, etc.';

CREATE TABLE catalog.ticket_states (
    id   INTEGER      NOT NULL,
    name VARCHAR(100) NOT NULL,
    CONSTRAINT ticket_states_pkey PRIMARY KEY (id)
);
COMMENT ON TABLE catalog.ticket_states IS 'Estados de ticket: activo, usado, cancelado';

CREATE TABLE catalog.payment_methods (
    id   INTEGER      NOT NULL,
    name VARCHAR(100) NOT NULL,
    CONSTRAINT payment_methods_pkey PRIMARY KEY (id)
);
COMMENT ON TABLE catalog.payment_methods IS 'Métodos de pago: efectivo, transferencia, tarjeta, Nequi, Daviplata';

CREATE TABLE catalog.order_statuses (
    id   INTEGER      NOT NULL,
    name VARCHAR(100) NOT NULL,
    CONSTRAINT order_statuses_pkey PRIMARY KEY (id)
);
COMMENT ON TABLE catalog.order_statuses IS 'Estados de orden: pendiente, pagada, cancelada, reembolsada';


-- ============================================================
--  SCHEMA: core
--  Entidades principales del negocio
-- ============================================================

CREATE TABLE core.users (
    id            INTEGER      NOT NULL GENERATED ALWAYS AS IDENTITY,
    username      VARCHAR(255) NOT NULL,
    email         VARCHAR(255) NOT NULL,
    phone_number  VARCHAR(50)  NOT NULL,
    password_hash TEXT         NOT NULL,
    type_user_id  INTEGER      NOT NULL,
    fcm_token     TEXT,
    is_active     BOOLEAN      NOT NULL DEFAULT TRUE,
    created_at    TIMESTAMP    NOT NULL DEFAULT CURRENT_TIMESTAMP,
    updated_at    TIMESTAMP    NOT NULL DEFAULT CURRENT_TIMESTAMP,

    CONSTRAINT users_pkey            PRIMARY KEY (id),
    CONSTRAINT users_email_key       UNIQUE (email),
    CONSTRAINT users_phone_key       UNIQUE (phone_number),
    CONSTRAINT chk_users_email_format
        CHECK (email ~ '^[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}$'),
    CONSTRAINT chk_users_created_at
        CHECK (created_at <= CURRENT_TIMESTAMP),
    CONSTRAINT fk_users_type_user
        FOREIGN KEY (type_user_id) REFERENCES catalog.type_users (id)
);
COMMENT ON COLUMN core.users.fcm_token     IS 'Token de Firebase Cloud Messaging para notificaciones push';
COMMENT ON COLUMN core.users.password_hash IS 'Hash bcrypt de la contraseña';
COMMENT ON COLUMN core.users.is_active     IS 'FALSE = usuario desactivado por admin, no puede hacer login';

CREATE INDEX idx_users_type_user ON core.users (type_user_id);
CREATE INDEX idx_users_email     ON core.users (email);


CREATE TABLE core.events (
    id              INTEGER       NOT NULL GENERATED ALWAYS AS IDENTITY,
    name            VARCHAR(300)  NOT NULL,
    description     TEXT,
    flyer_url       TEXT,
    start_time      TIMESTAMP     NOT NULL,
    end_time        TIMESTAMP     NOT NULL,
    event_state_id  INTEGER,
    created_by      INTEGER,
    created_at      TIMESTAMP     NOT NULL DEFAULT CURRENT_TIMESTAMP,
    updated_at      TIMESTAMP     NOT NULL DEFAULT CURRENT_TIMESTAMP,

    CONSTRAINT events_pkey       PRIMARY KEY (id),
    CONSTRAINT chk_events_time   CHECK (start_time < end_time),
    CONSTRAINT fk_events_state
        FOREIGN KEY (event_state_id) REFERENCES catalog.event_states (id),
    CONSTRAINT fk_events_created_by
        FOREIGN KEY (created_by) REFERENCES core.users (id)
);
COMMENT ON COLUMN core.events.flyer_url  IS 'URL pública del flyer/imagen del evento (almacenado en Supabase Storage)';
COMMENT ON COLUMN core.events.created_by IS 'Admin que creó el evento';

CREATE INDEX idx_events_state      ON core.events (event_state_id);
CREATE INDEX idx_events_start_time ON core.events (start_time);


CREATE TABLE core.dico_tables (
    id              INTEGER  NOT NULL GENERATED ALWAYS AS IDENTITY,
    number          INTEGER  NOT NULL,
    table_type_id   INTEGER  NOT NULL,
    capacity        INTEGER  NOT NULL,
    table_state_id  INTEGER  NOT NULL,

    CONSTRAINT dico_tables_pkey       PRIMARY KEY (id),
    CONSTRAINT dico_tables_number_key UNIQUE (number),
    CONSTRAINT chk_tables_capacity    CHECK (capacity > 0),
    CONSTRAINT fk_tables_type
        FOREIGN KEY (table_type_id)  REFERENCES catalog.table_types (id),
    CONSTRAINT fk_tables_state
        FOREIGN KEY (table_state_id) REFERENCES catalog.table_states (id)
);
COMMENT ON TABLE core.dico_tables IS 'Mesas físicas de la discoteca';


CREATE TABLE core.type_tickets (
    id                 INTEGER        NOT NULL GENERATED ALWAYS AS IDENTITY,
    name               VARCHAR(200)   NOT NULL,
    event_id           INTEGER        NOT NULL,
    available_quantity INTEGER        NOT NULL,
    max_override       INTEGER,
    price              NUMERIC(10,2)  NOT NULL,

    CONSTRAINT type_tickets_pkey     PRIMARY KEY (id),
    CONSTRAINT chk_type_tickets_qty  CHECK (available_quantity >= 0),
    CONSTRAINT chk_type_tickets_price CHECK (price >= 0),
    CONSTRAINT chk_type_tickets_override
        CHECK (max_override IS NULL OR max_override > available_quantity),
    CONSTRAINT fk_type_tickets_event
        FOREIGN KEY (event_id) REFERENCES core.events (id)
);
COMMENT ON TABLE core.type_tickets IS 'Tipos de entrada por evento (General, VIP, Early bird, etc.)';

CREATE INDEX idx_type_tickets_event ON core.type_tickets (event_id);


CREATE TABLE core.table_prices (
    id        INTEGER        NOT NULL GENERATED ALWAYS AS IDENTITY,
    table_id  INTEGER        NOT NULL,
    event_id  INTEGER        NOT NULL,
    price     NUMERIC(10,2)  NOT NULL,

    CONSTRAINT table_prices_pkey              PRIMARY KEY (id),
    CONSTRAINT uq_table_prices_table_event    UNIQUE (table_id, event_id),
    CONSTRAINT chk_table_prices_price         CHECK (price >= 0),
    CONSTRAINT fk_table_prices_table
        FOREIGN KEY (table_id) REFERENCES core.dico_tables (id),
    CONSTRAINT fk_table_prices_event
        FOREIGN KEY (event_id) REFERENCES core.events (id)
);
COMMENT ON TABLE core.table_prices IS 'Precio de reserva de cada mesa según el evento';

CREATE INDEX idx_table_prices_table ON core.table_prices (table_id);
CREATE INDEX idx_table_prices_event ON core.table_prices (event_id);


-- ============================================================
--  SCHEMA: transactions
--  Flujo de compra: orden → ítems → pago
-- ============================================================

CREATE TABLE transactions.orders (
    id          INTEGER        NOT NULL GENERATED ALWAYS AS IDENTITY,
    user_id     INTEGER        NOT NULL,
    ordered_at  TIMESTAMP      NOT NULL DEFAULT CURRENT_TIMESTAMP,
    total       NUMERIC(10,2)  NOT NULL DEFAULT 0,
    status      VARCHAR(20)    NOT NULL DEFAULT 'pending',
    notes       TEXT,
    created_at  TIMESTAMP      NOT NULL DEFAULT CURRENT_TIMESTAMP,
    updated_at  TIMESTAMP      NOT NULL DEFAULT CURRENT_TIMESTAMP,

    CONSTRAINT orders_pkey      PRIMARY KEY (id),
    CONSTRAINT chk_orders_total CHECK (total >= 0),
    CONSTRAINT chk_orders_status
        CHECK (status IN ('pending', 'paid', 'cancelled', 'refunded')),
    CONSTRAINT fk_orders_user
        FOREIGN KEY (user_id) REFERENCES core.users (id)
);
COMMENT ON COLUMN transactions.orders.notes  IS 'Notas del admin al confirmar o cancelar la orden';
COMMENT ON COLUMN transactions.orders.status IS 'pending=esperando pago, paid=confirmado por admin, cancelled, refunded';

CREATE INDEX idx_orders_user   ON transactions.orders (user_id);
CREATE INDEX idx_orders_status ON transactions.orders (status);


CREATE TABLE transactions.reservations (
    id                    INTEGER    NOT NULL GENERATED ALWAYS AS IDENTITY,
    reservation_state_id  INTEGER    NOT NULL,
    user_id               INTEGER    NOT NULL,
    table_id              INTEGER    NOT NULL,
    event_id              INTEGER,
    reserved_at           TIMESTAMP  NOT NULL DEFAULT CURRENT_TIMESTAMP,
    expires_at            TIMESTAMP,
    created_at            TIMESTAMP  NOT NULL DEFAULT CURRENT_TIMESTAMP,
    updated_at            TIMESTAMP  NOT NULL DEFAULT CURRENT_TIMESTAMP,

    CONSTRAINT reservations_pkey PRIMARY KEY (id),
    CONSTRAINT fk_reservations_state
        FOREIGN KEY (reservation_state_id) REFERENCES catalog.reservation_states (id),
    CONSTRAINT fk_reservations_user
        FOREIGN KEY (user_id)  REFERENCES core.users (id),
    CONSTRAINT fk_reservations_table
        FOREIGN KEY (table_id) REFERENCES core.dico_tables (id),
    CONSTRAINT fk_reservations_event
        FOREIGN KEY (event_id) REFERENCES core.events (id)
);
COMMENT ON COLUMN transactions.reservations.expires_at IS 'NULL = sin expiración automática. Se usa para bloqueos temporales antes de pago';

CREATE INDEX idx_reservations_user    ON transactions.reservations (user_id);
CREATE INDEX idx_reservations_table   ON transactions.reservations (table_id);
CREATE INDEX idx_reservations_event   ON transactions.reservations (event_id);
CREATE INDEX idx_reservations_state   ON transactions.reservations (reservation_state_id);
CREATE INDEX idx_reservations_expires ON transactions.reservations (expires_at)
    WHERE expires_at IS NOT NULL;

CREATE UNIQUE INDEX uq_active_reservation_per_table
    ON transactions.reservations (table_id)
    WHERE reservation_state_id IN (1, 2);


CREATE TABLE transactions.tickets (
    id               INTEGER    NOT NULL GENERATED ALWAYS AS IDENTITY,
    user_id          INTEGER    NOT NULL,
    type_ticket_id   INTEGER    NOT NULL,
    ticket_state_id  INTEGER    NOT NULL,
    created_at       TIMESTAMP  NOT NULL DEFAULT CURRENT_TIMESTAMP,
    updated_at       TIMESTAMP  NOT NULL DEFAULT CURRENT_TIMESTAMP,

    CONSTRAINT tickets_pkey PRIMARY KEY (id),
    CONSTRAINT fk_tickets_user
        FOREIGN KEY (user_id)         REFERENCES core.users (id),
    CONSTRAINT fk_tickets_type
        FOREIGN KEY (type_ticket_id)  REFERENCES core.type_tickets (id),
    CONSTRAINT fk_tickets_state
        FOREIGN KEY (ticket_state_id) REFERENCES catalog.ticket_states (id)
);

CREATE INDEX idx_tickets_user  ON transactions.tickets (user_id);
CREATE INDEX idx_tickets_type  ON transactions.tickets (type_ticket_id);
CREATE INDEX idx_tickets_state ON transactions.tickets (ticket_state_id);


CREATE TABLE transactions.order_details (
    id              INTEGER        NOT NULL GENERATED ALWAYS AS IDENTITY,
    order_id        INTEGER        NOT NULL,
    ticket_id       INTEGER,
    reservation_id  INTEGER,
    type_ticket_id  INTEGER,
    table_id        INTEGER,
    quantity        INTEGER        NOT NULL DEFAULT 1,
    unit_price      NUMERIC(10,2)  NOT NULL,
    discount        NUMERIC(10,2)  NOT NULL DEFAULT 0,

    CONSTRAINT order_details_pkey         PRIMARY KEY (id),
    CONSTRAINT chk_order_details_qty      CHECK (quantity > 0),
    CONSTRAINT chk_order_details_discount CHECK (discount >= 0),
    CONSTRAINT chk_order_details_price    CHECK (unit_price >= 0),
    CONSTRAINT chk_order_details_item
        CHECK (ticket_id IS NOT NULL OR reservation_id IS NOT NULL),
    CONSTRAINT fk_order_details_order
        FOREIGN KEY (order_id)       REFERENCES transactions.orders (id),
    CONSTRAINT fk_order_details_ticket
        FOREIGN KEY (ticket_id)      REFERENCES transactions.tickets (id),
    CONSTRAINT fk_order_details_reservation
        FOREIGN KEY (reservation_id) REFERENCES transactions.reservations (id)
);
COMMENT ON CONSTRAINT chk_order_details_item ON transactions.order_details
    IS 'Todo detalle debe referenciar al menos un ticket o una reserva';

CREATE INDEX idx_order_details_order       ON transactions.order_details (order_id);
CREATE INDEX idx_order_details_ticket      ON transactions.order_details (ticket_id);
CREATE INDEX idx_order_details_reservation ON transactions.order_details (reservation_id);


CREATE TABLE transactions.payments (
    id                INTEGER        NOT NULL GENERATED ALWAYS AS IDENTITY,
    order_id          INTEGER        NOT NULL,
    payment_method_id INTEGER        NOT NULL,
    amount            NUMERIC(10,2)  NOT NULL,
    status            VARCHAR(20)    NOT NULL DEFAULT 'pending',
    voucher_url       TEXT,
    reference_number  TEXT,
    confirmed_by      INTEGER,
    confirmed_at      TIMESTAMP,
    notes             TEXT,
    created_at        TIMESTAMP      NOT NULL DEFAULT CURRENT_TIMESTAMP,

    CONSTRAINT payments_pkey         PRIMARY KEY (id),
    CONSTRAINT chk_payments_amount   CHECK (amount >= 0),
    CONSTRAINT chk_payments_status
        CHECK (status IN ('pending', 'confirmed', 'rejected', 'refunded')),
    CONSTRAINT fk_payments_order
        FOREIGN KEY (order_id)     REFERENCES transactions.orders (id),
    CONSTRAINT fk_payments_method
        FOREIGN KEY (payment_method_id) REFERENCES catalog.payment_methods (id),
    CONSTRAINT fk_payments_confirmed_by
        FOREIGN KEY (confirmed_by) REFERENCES core.users (id)
);
COMMENT ON COLUMN transactions.payments.voucher_url    IS 'URL del comprobante subido por el cliente a Supabase Storage';
COMMENT ON COLUMN transactions.payments.reference_number IS 'Número de referencia del comprobante bancario';
COMMENT ON COLUMN transactions.payments.confirmed_by   IS 'Admin que confirmó el pago manualmente';
COMMENT ON COLUMN transactions.payments.confirmed_at   IS 'Cuándo fue confirmado el pago';
COMMENT ON COLUMN transactions.payments.notes          IS 'Notas del admin al confirmar o rechazar el pago';

CREATE INDEX idx_payments_order  ON transactions.payments (order_id);
CREATE INDEX idx_payments_status ON transactions.payments (status);


-- ============================================================
--  SCHEMA: audit
--  Trazabilidad de cambios en datos críticos
-- ============================================================

CREATE TABLE audit.audit_logs (
    id           BIGINT       NOT NULL GENERATED ALWAYS AS IDENTITY,
    table_name   VARCHAR(100) NOT NULL,
    record_id    INTEGER      NOT NULL,
    action       VARCHAR(10)  NOT NULL,
    old_data     JSONB,
    new_data     JSONB,
    user_id      INTEGER,
    performed_at TIMESTAMP    NOT NULL DEFAULT CURRENT_TIMESTAMP,

    CONSTRAINT audit_logs_pkey          PRIMARY KEY (id),
    CONSTRAINT audit_logs_action_check
        CHECK (action IN ('INSERT', 'UPDATE', 'DELETE'))
);

CREATE INDEX idx_audit_logs_table_record ON audit.audit_logs (table_name, record_id);
CREATE INDEX idx_audit_logs_performed_at ON audit.audit_logs (performed_at);
CREATE INDEX idx_audit_logs_user         ON audit.audit_logs (user_id);


-- ============================================================
--  SCHEMA: system
--  Configuración y logs administrativos
-- ============================================================

CREATE TABLE system.admin_actions_log (
    id          INTEGER    NOT NULL GENERATED ALWAYS AS IDENTITY,
    admin_id    INTEGER    NOT NULL,
    action      TEXT       NOT NULL,
    payload     JSONB,
    ip_address  TEXT,
    user_agent  TEXT,
    created_at  TIMESTAMP  NOT NULL DEFAULT NOW(),

    CONSTRAINT admin_actions_log_pkey PRIMARY KEY (id),
    CONSTRAINT fk_admin_actions_user
        FOREIGN KEY (admin_id) REFERENCES core.users (id)
);
COMMENT ON TABLE system.admin_actions_log IS 'Registro de acciones administrativas: crear evento, confirmar pago, cambiar estado de mesa, etc.';

CREATE INDEX idx_admin_actions_admin ON system.admin_actions_log (admin_id);
CREATE INDEX idx_admin_actions_at    ON system.admin_actions_log (created_at);


CREATE TABLE system.app_config (
    key         VARCHAR(100) NOT NULL,
    value       TEXT         NOT NULL,
    description TEXT,
    updated_at  TIMESTAMP    NOT NULL DEFAULT NOW(),

    CONSTRAINT app_config_pkey PRIMARY KEY (key)
);
COMMENT ON TABLE system.app_config IS 'Configuración global de la app: tiempo de expiración de reservas, nombre del local, etc.';


-- ============================================================
--  DATOS SEMILLA (SEED DATA)
--  Valores iniciales de catálogos
-- ============================================================

-- Roles de usuario
INSERT INTO catalog.type_users (id, name) VALUES
    (1, 'cliente'),
    (2, 'admin'),
    (3, 'staff');

-- Estados de evento
INSERT INTO catalog.event_states (id, name) VALUES
    (1, 'activo'),
    (2, 'cancelado'),
    (3, 'finalizado'),
    (4, 'borrador');

-- Estados de reserva
INSERT INTO catalog.reservation_states (id, name) VALUES
    (1, 'pendiente'),
    (2, 'confirmada'),
    (3, 'expirada'),
    (4, 'cancelada');

-- Estados de mesa
INSERT INTO catalog.table_states (id, name) VALUES
    (1, 'disponible'),
    (2, 'reservada'),
    (3, 'fuera_de_servicio');

-- Tipos de mesa
INSERT INTO catalog.table_types (id, name) VALUES
    (1, 'regular'),
    (2, 'vip'),
    (3, 'terraza'),
    (4, 'privada');

-- Estados de ticket
INSERT INTO catalog.ticket_states (id, name) VALUES
    (1, 'activo'),
    (2, 'usado'),
    (3, 'cancelado');

-- Métodos de pago (manual, sin pasarela)
INSERT INTO catalog.payment_methods (id, name) VALUES
    (1, 'efectivo'),
    (2, 'transferencia_bancaria'),
    (3, 'nequi'),
    (4, 'daviplata'),
    (5, 'tarjeta_credito'),
    (6, 'tarjeta_debito');

-- Estados de orden
INSERT INTO catalog.order_statuses (id, name) VALUES
    (1, 'pending'),
    (2, 'paid'),
    (3, 'cancelled'),
    (4, 'refunded');

-- Configuración inicial de la app
INSERT INTO system.app_config (key, value, description) VALUES
    ('reservation_expiry_minutes', '30',      'Minutos antes de que expire una reserva sin pagar'),
    ('max_tickets_per_user',       '10',       'Máximo de tickets que puede comprar un usuario por evento'),
    ('venue_name',                 'Discoteca', 'Nombre del local que aparece en la app'),
    ('venue_capacity',             '500',       'Aforo máximo del establecimiento');


-- ============================================================
--  FUNCIÓN DE AUDITORÍA AUTOMÁTICA
--  Trigger que registra INSERT/UPDATE/DELETE en tablas críticas
-- ============================================================

CREATE OR REPLACE FUNCTION audit.log_changes()
RETURNS TRIGGER
LANGUAGE plpgsql
SECURITY DEFINER
AS $$
BEGIN
    IF TG_OP = 'DELETE' THEN
        INSERT INTO audit.audit_logs (table_name, record_id, action, old_data, new_data, user_id)
        VALUES (TG_TABLE_NAME, OLD.id, 'DELETE', to_jsonb(OLD), NULL,
                NULLIF(current_setting('app.current_user_id', TRUE), '')::INTEGER);
        RETURN OLD;
    ELSIF TG_OP = 'UPDATE' THEN
        INSERT INTO audit.audit_logs (table_name, record_id, action, old_data, new_data, user_id)
        VALUES (TG_TABLE_NAME, NEW.id, 'UPDATE', to_jsonb(OLD), to_jsonb(NEW),
                NULLIF(current_setting('app.current_user_id', TRUE), '')::INTEGER);
        RETURN NEW;
    ELSIF TG_OP = 'INSERT' THEN
        INSERT INTO audit.audit_logs (table_name, record_id, action, old_data, new_data, user_id)
        VALUES (TG_TABLE_NAME, NEW.id, 'INSERT', NULL, to_jsonb(NEW),
                NULLIF(current_setting('app.current_user_id', TRUE), '')::INTEGER);
        RETURN NEW;
    END IF;
    RETURN NULL;
END;
$$;

-- Aplicar trigger a tablas críticas
CREATE TRIGGER trg_audit_events
    AFTER INSERT OR UPDATE OR DELETE ON core.events
    FOR EACH ROW EXECUTE FUNCTION audit.log_changes();

CREATE TRIGGER trg_audit_reservations
    AFTER INSERT OR UPDATE OR DELETE ON transactions.reservations
    FOR EACH ROW EXECUTE FUNCTION audit.log_changes();

CREATE TRIGGER trg_audit_payments
    AFTER INSERT OR UPDATE OR DELETE ON transactions.payments
    FOR EACH ROW EXECUTE FUNCTION audit.log_changes();

CREATE TRIGGER trg_audit_orders
    AFTER INSERT OR UPDATE OR DELETE ON transactions.orders
    FOR EACH ROW EXECUTE FUNCTION audit.log_changes();


-- ============================================================
--  FUNCIÓN DE updated_at AUTOMÁTICO
-- ============================================================

CREATE OR REPLACE FUNCTION core.set_updated_at()
RETURNS TRIGGER
LANGUAGE plpgsql
AS $$
BEGIN
    NEW.updated_at = CURRENT_TIMESTAMP;
    RETURN NEW;
END;
$$;

CREATE TRIGGER trg_updated_at_users
    BEFORE UPDATE ON core.users
    FOR EACH ROW EXECUTE FUNCTION core.set_updated_at();

CREATE TRIGGER trg_updated_at_events
    BEFORE UPDATE ON core.events
    FOR EACH ROW EXECUTE FUNCTION core.set_updated_at();

CREATE TRIGGER trg_updated_at_orders
    BEFORE UPDATE ON transactions.orders
    FOR EACH ROW EXECUTE FUNCTION core.set_updated_at();

CREATE TRIGGER trg_updated_at_reservations
    BEFORE UPDATE ON transactions.reservations
    FOR EACH ROW EXECUTE FUNCTION core.set_updated_at();

CREATE TRIGGER trg_updated_at_tickets
    BEFORE UPDATE ON transactions.tickets
    FOR EACH ROW EXECUTE FUNCTION core.set_updated_at();


-- ============================================================
--  VISTAS ÚTILES
-- ============================================================

-- Vista: eventos activos con conteo de tickets disponibles
CREATE OR REPLACE VIEW core.v_active_events AS
SELECT
    e.id,
    e.name,
    e.description,
    e.flyer_url,
    e.start_time,
    e.end_time,
    es.name        AS state,
    COUNT(tt.id)   AS ticket_types_count,
    SUM(tt.available_quantity) AS total_tickets_available
FROM core.events e
JOIN catalog.event_states es ON es.id = e.event_state_id
LEFT JOIN core.type_tickets tt ON tt.event_id = e.id
WHERE e.event_state_id = 1   -- solo activos
GROUP BY e.id, e.name, e.description, e.flyer_url,
         e.start_time, e.end_time, es.name;

-- Vista: mesas con su tipo, estado y precio por evento
CREATE OR REPLACE VIEW core.v_tables_with_prices AS
SELECT
    dt.id            AS table_id,
    dt.number        AS table_number,
    tt.name          AS table_type,
    ts.name          AS table_state,
    dt.capacity,
    tp.event_id,
    tp.price
FROM core.dico_tables dt
JOIN catalog.table_types  tt ON tt.id = dt.table_type_id
JOIN catalog.table_states ts ON ts.id = dt.table_state_id
LEFT JOIN core.table_prices tp ON tp.table_id = dt.id;

-- Vista: pagos pendientes de confirmación por admin
CREATE OR REPLACE VIEW transactions.v_pending_payments AS
SELECT
    p.id              AS payment_id,
    p.amount,
    p.status,
    p.voucher_url,
    p.reference_number,
    p.created_at      AS payment_date,
    pm.name           AS payment_method,
    o.id              AS order_id,
    o.total           AS order_total,
    u.id              AS user_id,
    u.username,
    u.email,
    u.phone_number
FROM transactions.payments p
JOIN catalog.payment_methods pm ON pm.id = p.payment_method_id
JOIN transactions.orders     o  ON o.id  = p.order_id
JOIN core.users              u  ON u.id  = o.user_id
WHERE p.status = 'pending'
ORDER BY p.created_at ASC;

-- Vista: historial completo de reservas de un usuario
CREATE OR REPLACE VIEW transactions.v_user_reservations AS
SELECT
    r.id               AS reservation_id,
    r.user_id,
    u.username,
    r.table_id,
    dt.number          AS table_number,
    tt.name            AS table_type,
    e.name             AS event_name,
    e.start_time,
    rs.name            AS reservation_state,
    r.reserved_at,
    r.expires_at,
    tp.price           AS table_price
FROM transactions.reservations r
JOIN core.users             u   ON u.id   = r.user_id
JOIN core.dico_tables       dt  ON dt.id  = r.table_id
JOIN catalog.table_types    tt  ON tt.id  = dt.table_type_id
JOIN catalog.reservation_states rs ON rs.id = r.reservation_state_id
LEFT JOIN core.events       e   ON e.id   = r.event_id
LEFT JOIN core.table_prices tp  ON tp.table_id = r.table_id
                                AND tp.event_id = r.event_id;


-- ============================================================
--  FIN DEL SCRIPT
-- ============================================================
