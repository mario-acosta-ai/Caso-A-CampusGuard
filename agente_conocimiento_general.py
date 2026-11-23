"""
UNIVERSIDAD MILITAR NUEVA GRANADA (UMNG)
Programa de Ingeniería Informática Virtual - Inteligencia Artificial I
Fase 3 / Taller 03: Agentes Basados en Conocimiento (KB-Agent) y Motor de Reglas

Integrantes Grupo D:
- Angie Valentina González Mongui (200616)
- Jonhsef Estiven Acosta Quitián (200563)
- Juan Guillermo Pulido Moreno (200580)
- Mario Alberto Acosta Prieto (200571)
- Omar David Rojas Rodríguez (200575)

Este módulo implementa la arquitectura declarativa de un Agente Basado en Conocimiento,
separando explícitamente la Base de Conocimiento (hechos y reglas) del Motor de Inferencia
(Encadenamiento Hacia Adelante / Modus Ponens), e implementando el ciclo clásico TELL-ASK
aplicado al Reto Multiparadigma Cloud (Punto A) y al caso CampusGuard UMNG (Punto B).
"""

from typing import List, Dict, Set, Optional


# =============================================================================
# BLOQUE 1: ESTRUCTURA DE REGLAS LÓGICAS (IMPLICACIONES CONDICIONALES)
# =============================================================================

class ReglaConocimiento:
    """
    Representa una regla de inferencia lógica en forma de implicación (P1 ^ P2 ^ ... -> Q).
    Si todas las premisas se encuentran en la Base de Conocimiento, se deduce la consecuencia.
    """
    def __init__(self, premisas: List[str], consecuencia: str, descripcion: str = ""):
        self.premisas = premisas          # Lista de proposiciones atómicas requeridas (antecedente)
        self.consecuencia = consecuencia  # Proposición nueva deducida (consecuente)
        self.descripcion = descripcion    # Justificación normativa en lenguaje natural

    def __repr__(self) -> str:
        condiciones = " Y ".join(self.premisas)
        return f"SI ({condiciones}) ENTONCES '{self.consecuencia}'"


# =============================================================================
# BLOQUE 2: BASE DE CONOCIMIENTO (KNOWLEDGE BASE - KB) Y MOTOR DE INFERENCIA
# =============================================================================

class BaseDeConocimiento:
    """
    Componente Declarativo: Almacena los hechos observados/deducidos y las reglas
    institucionales sin acoplarlas a estructuras imperativas rígidas (if-else).
    Mantiene memoria persistente de los hechos verdaderos a lo largo del tiempo t.
    """
    def __init__(self):
        # Conjunto de hechos verdaderos conocidos (evita duplicados automáticamente)
        self.hechos: Set[str] = set()
        # Lista ordenada de reglas lógicas registradas en el sistema
        self.reglas: List[ReglaConocimiento] = []

    def tell_hecho(self, hecho: str):
        """
        Operación TELL (Perceptos/Hechos): Inserta un hecho atómico verdadero en la KB.
        """
        if hecho not in self.hechos:
            self.hechos.add(hecho)
            print(f"   [TELL -> KB]: Hecho registrado -> '{hecho}'")

    def tell_regla(self, premisas: List[str], consecuencia: str, descripcion: str = ""):
        """
        Operación TELL (Reglas): Registra una regla condicional normativa en la KB.
        """
        regla = ReglaConocimiento(premisas, consecuencia, descripcion)
        self.reglas.append(regla)
        print(f"   [TELL -> KB]: Regla registrada -> {regla}")

    def ejecutar_inferencia(self):
        """
        Motor de Inferencia: Aplica Encadenamiento Hacia Adelante (Forward Chaining)
        mediante la regla de deducción Modus Ponens hasta alcanzar un punto fijo.
        """
        nuevas_deducciones = True
        while nuevas_deducciones:
            nuevas_deducciones = False
            for regla in self.reglas:
                # Verifica si la consecuencia aún no ha sido inferida
                if regla.consecuencia not in self.hechos:
                    # Comprueba si TODAS las premisas se satisfacen en la KB actual
                    if all(premisa in self.hechos for premisa in regla.premisas):
                        self.hechos.add(regla.consecuencia)
                        print(f"   [MOTOR INFERENCIA - Modus Ponens]:")
                        print(f"      Regla activada : {regla}")
                        if regla.descripcion:
                            print(f"      Justificación  : {regla.descripcion}")
                        print(f"      -> Hecho deducido: '{regla.consecuencia}'")
                        nuevas_deducciones = True

    def ask(self, consulta: str) -> bool:
        """
        Operación ASK: Actualiza las deducciones lógicas e interroga si la consulta
        es consecuencia lógica de la Base de Conocimiento (KB |= consulta).
        """
        self.ejecutar_inferencia()
        return consulta in self.hechos


# =============================================================================
# BLOQUE 3: AGENTES BASADOS EN CONOCIMIENTO (CICLO TELL-ASK)
# =============================================================================

class AgenteBasadoEnConocimiento:
    """
    Agente Racional Simbólico que opera mediante el ciclo percepción -> TELL -> ASK -> acción:
    1. Percibe el estado actual del entorno.
    2. Actualiza la KB mediante operaciones TELL.
    3. Consulta acciones autorizadas mediante operaciones ASK.
    4. Registra la acción ejecutada en la KB para mantener trazabilidad temporal.
    """
    def __init__(self, kb: BaseDeConocimiento):
        self.kb = kb
        self.paso_tiempo = 0

    def percibir(self, perceptos: Dict[str, bool]):
        """
        Ingesta los perceptos verdaderos del instante actual t hacia la KB.
        """
        print(f"\n===========================================================")
        print(f" [TIEMPO t = {self.paso_tiempo}] INGESTIÓN DE PERCEPTOS (TELL)")
        print(f"===========================================================")
        for concepto, estado in perceptos.items():
            if estado:
                self.kb.tell_hecho(concepto)

    def decidir_accion(self, catalogo_acciones: Dict[str, str]) -> Optional[str]:
        """
        Evalúa mediante consultas ASK qué nueva intervención está lógicamente justificada.
        :param catalogo_acciones: Diccionario {"NombreAccion": "CondicionRequeridaEnKB"}
        """
        print(f"\n--- EVALUACIÓN DE POLÍTICAS MEDIANTE CONSULTAS ASK ---")
        accion_elegida = None

        for accion, condicion_requerida in catalogo_acciones.items():
            es_valida = self.kb.ask(condicion_requerida)
            ya_ejecutada = f"Accion_{accion}_Ejecutada" in self.kb.hechos
            print(f"  Consulta ASK: ¿KB |= '{condicion_requerida}' para '{accion}'? -> {es_valida}")
            if es_valida and not ya_ejecutada and accion_elegida is None:
                accion_elegida = accion

        if accion_elegida:
            print(f"\n  ==> [DECISIÓN RACIONAL]: Ejecutar '{accion_elegida}'")
            self.kb.tell_hecho(f"Accion_{accion_elegida}_Ejecutada")
            self.kb.tell_hecho(f"Accion_{accion_elegida}_t{self.paso_tiempo}")
        else:
            print(f"\n  ==> [DECISIÓN RACIONAL]: Ninguna acción nueva autorizada. Mantener monitoreo.")

        self.paso_tiempo += 1
        return accion_elegida


class AgenteDespliegue(AgenteBasadoEnConocimiento):
    """
    Especialización del Agente Basado en Conocimiento para el Punto A:
    Automatización de pase a producción y políticas de seguridad en infraestructura Cloud.
    """
    def __init__(self):
        super().__init__(BaseDeConocimiento())
        # Carga declarativa de las 3 reglas de negocio del despliegue Cloud
        self.kb.tell_regla(
            premisas=["Pasa_Pruebas_Unitarias", "Seguridad_Estatica_OK"],
            consecuencia="Pre_Produccion_Habilitada",
            descripcion="Regla 1: Pruebas unitarias y seguridad estática habilitan pre-producción."
        )
        self.kb.tell_regla(
            premisas=["Pre_Produccion_Habilitada", "Aprobacion_Lider_Tecnico"],
            consecuencia="Despliegue_Produccion_Autorizado",
            descripcion="Regla 2: Pre-producción más aprobación del líder autorizan paso a producción."
        )
        self.kb.tell_regla(
            premisas=["Despliegue_Produccion_Autorizado"],
            consecuencia="Activar_MFA_Obligatorio",
            descripcion="Regla 3: Todo pase a producción exige autenticación multifactor (MFA)."
        )


# =============================================================================
# BLOQUE 4: SIMULACIÓN PUNTO A (RETO MULTIPARADIGMA CLOUD)
# =============================================================================

def simular_punto_a_cloud():
    print("===========================================================================")
    print("  PUNTO A (ENFOQUE 3): AGENTE DE DESPLIEGUE SEGURO EN CLOUD (MICROSERVICIO_AUTH)")
    print("===========================================================================")

    agente_cloud = AgenteDespliegue()

    catalogo_cloud = {
        "Desplegar_En_Produccion_Con_MFA": "Activar_MFA_Obligatorio"
    }

    # Perceptos de validación para la entidad Microservicio_Auth
    perceptos_microservicio = {
        "Pasa_Pruebas_Unitarias": True,
        "Seguridad_Estatica_OK": True,
        "Aprobacion_Lider_Tecnico": True
    }

    agente_cloud.percibir(perceptos_microservicio)
    agente_cloud.decidir_accion(catalogo_cloud)


# =============================================================================
# BLOQUE 5: SIMULACIÓN PUNTO B (CASO DE ESTUDIO CAMPUSGUARD UMNG - GRUPO D)
# =============================================================================

def simular_punto_b_campusguard():
    print("\n===========================================================================")
    print("  PUNTO B: AGENTE BASADO EN CONOCIMIENTO - CAMPUSGUARD UMNG (GRUPO D)")
    print("===========================================================================")

    # 1. Instanciación de la Base de Conocimiento y del Agente CampusGuard
    kb_campus = BaseDeConocimiento()
    agente_campus = AgenteBasadoEnConocimiento(kb_campus)

    # 2. Carga de Políticas Normativas (Capa Declarativa - 4 Reglas Institucionales)
    # Orden coherente con el ciclo académico y administrativo de la UMNG:
    # Primero acompañamiento pedagógico/curricular (con LMS activo), luego restricción financiera.
    print("\n[CONFIGURACIÓN KB]: Registro de políticas institucionales en la capa declarativa")
    kb_campus.tell_regla(
        premisas=["Promedio_Bajo", "Ausentismo_Alto"],
        consecuencia="Alerta_Riesgo_Academico",
        descripcion="Bajo rendimiento y alto ausentismo (> 40%) disparan alerta temprana (< 48h)."
    )
    kb_campus.tell_regla(
        premisas=["Alerta_Riesgo_Academico"],
        consecuencia="Activar_Tutor_Acompanamiento",
        descripcion="Toda alerta de riesgo académico obliga a asignar tutor pedagógico y remitir a Bienestar."
    )
    kb_campus.tell_regla(
        premisas=["Alerta_Riesgo_Academico", "Materias_Criticas_Mayor_2"],
        consecuencia="Requiere_Reestructurar_Carga",
        descripcion="Alerta académica con >= 2 materias críticas habilita reestructuración de créditos."
    )
    kb_campus.tell_regla(
        premisas=["Pago_Matricula_Pendiente", "Plazo_Vencido"],
        consecuencia="Bloqueo_Plataforma_LMS",
        descripcion="Mora financiera tras vencimiento de plazo genera restricción administrativa en LMS."
    )

    # Catálogo de intervenciones institucionales (Actuadores del Agente)
    acciones_campusguard = {
        "Asignar_Tutor_Pedagogico": "Activar_Tutor_Acompanamiento",
        "Reestructurar_Carga_Academica": "Requiere_Reestructurar_Carga",
        "Bloquear_Inscripcion_LMS": "Bloqueo_Plataforma_LMS"
    }

    # 3. Escenario t = 0 (Inicio de semestre): Monitoreo preventivo sin alertas críticas
    perceptos_t0 = {
        "Promedio_Bajo": True,
        "Ausentismo_Alto": False,
        "Pago_Matricula_Pendiente": True,
        "Plazo_Vencido": False,
        "Materias_Criticas_Mayor_2": False
    }
    agente_campus.percibir(perceptos_t0)
    agente_campus.decidir_accion(acciones_campusguard)

    # 4. Escenario t = 1 (Primeras semanas): Reporte de ausentismo > 40% -> Tutoría obligatoria
    perceptos_t1 = {
        "Ausentismo_Alto": True
    }
    agente_campus.percibir(perceptos_t1)
    agente_campus.decidir_accion(acciones_campusguard)

    # 5. Escenario t = 2 (Corte académico): Reporte de >= 2 materias críticas -> Ajuste de carga
    # Se ejecuta mientras el estudiante aún tiene acceso activo al LMS y consejería académica
    perceptos_t2 = {
        "Materias_Criticas_Mayor_2": True
    }
    agente_campus.percibir(perceptos_t2)
    agente_campus.decidir_accion(acciones_campusguard)

    # 6. Escenario t = 3 (Cierre plazo financiero): Vence plazo de matrícula pendiente -> Bloqueo LMS
    # Usa memoria persistente: 'Pago_Matricula_Pendiente' registrado en t=0 + 'Plazo_Vencido' en t=3
    perceptos_t3 = {
        "Plazo_Vencido": True
    }
    agente_campus.percibir(perceptos_t3)
    agente_campus.decidir_accion(acciones_campusguard)

    # Verificación directa ASK sobre la restricción en plataforma
    autoriza_bloqueo = kb_campus.ask("Bloqueo_Plataforma_LMS")
    print(f"\nVerificación directa ASK('Bloqueo_Plataforma_LMS'): {autoriza_bloqueo}")


if __name__ == "__main__":
    simular_punto_a_cloud()
    simular_punto_b_campusguard()