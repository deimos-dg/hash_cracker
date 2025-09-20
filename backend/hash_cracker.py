import hashlib
import re
import time
from concurrent.futures import ThreadPoolExecutor, as_completed
from typing import List, Dict, Optional
import logging

logger = logging.getLogger(__name__)


class AdvancedHashCracker:
    def __init__(self):
        self.common_passwords = self.load_common_passwords()
        self.stop_cracking = False
        self.stats = {
            'total_tested': 0,
            'start_time': None,
            'words_per_second': 0,
            'elapsed_time': 0
        }

    def load_common_passwords(self) -> List[str]:
        """Cargar contraseñas comunes"""
        return [
            "123456", "password", "123456789", "12345678", "12345",
            "1234567", "123123", "qwerty", "abc123", "111111",
            "admin", "password1", "1234", "1234567890", "letmein",
            "monkey", "shadow", "master", "666666", "123qwe",
            "welcome", "654321", "123321", "hello", "password123",
            "admin123", "user", "login", "passw0rd", "123abc",
            "test", "123", "1q2w3e4r", "qwerty123", "password12",
            "superman", "iloveyou", "starwars", "dragon", "sunshine",
            "princess", "trustno1", "000000", "password2", "123654",
            "charlie", "aa123456", "donald", "qwertyuiop", "123456a",
            "baseball", "football", "jordan", "letmein1", "12345678910",
            "password!", "adminadmin", "welcome123", "password1234",
            "123456789a", "123456789!", "qwe123", "admin1", "123123123",
            "123456789q", "123456789z", "123456789x", "123456789c",
            "123456789v", "123456789b", "123456789n", "123456789m",
            "zaq12wsx", "xdr56tfc", "!qaz2wsx", "1qaz2wsx", "1q2w3e4r5t",
            "qwerty1", "asdfgh", "zxcvbn", "asdfghjk", "qwerty123456",
            "password11", "password22", "password33", "password44",
            "admin1234", "admin12345", "root", "toor", "guest",
            "secret", "access", "super", "unknown", "anonymous"
        ]

    def identify_hash(self, hash_input: str) -> Dict:
        """Identificar hash con detalles"""
        hash_input = hash_input.strip()
        if not hash_input:
            return {'type': 'Unknown', 'length': 0, 'confidence': 'low'}

        hash_length = len(hash_input)

        # Detección por regex
        if re.match(r'^\$2[ayb]\$.{56}$', hash_input):
            hash_type = "bcrypt"
            confidence = "high"
        elif re.match(r'^[a-fA-F0-9]{32}$', hash_input):
            hash_type = "MD5"
            confidence = "high"
        elif re.match(r'^[a-fA-F0-9]{40}$', hash_input):
            hash_type = "SHA-1"
            confidence = "high"
        elif re.match(r'^[a-fA-F0-9]{64}$', hash_input):
            hash_type = "SHA-256"
            confidence = "high"
        elif re.match(r'^[a-fA-F0-9]{128}$', hash_input):
            hash_type = "SHA-512"
            confidence = "high"
        else:
            # Intentar identificar por longitud
            length_patterns = {
                32: "MD5",
                40: "SHA-1",
                64: "SHA-256",
                128: "SHA-512",
                56: "SHA-224",
                96: "SHA-384"
            }
            hash_type = length_patterns.get(hash_length, "Unknown")
            confidence = "medium" if hash_type != "Unknown" else "low"

        return {
            'type': hash_type,
            'length': hash_length,
            'confidence': confidence
        }

    def hash_function(self, algorithm: str, text: str) -> str:
        """Calcular hash"""
        text = text.encode('utf-8')

        algorithms = {
            "MD5": hashlib.md5,
            "SHA-1": hashlib.sa1,
            "SHA-256": hashlib.sha256,
            "SHA-512": hashlib.sha512
        }

        if algorithm in algorithms:
            return algorithms[algorithm](text).hexdigest()
        raise ValueError(f"Algoritmo no soportado: {algorithm}")

    def crack_hash(self, target_hash: str, algorithm: str, wordlist: List[str],
                   max_workers: int = 4) -> Dict:
        """Crackear hash con progreso"""
        self.stop_cracking = False
        self.stats = {
            'total_tested': 0,
            'start_time': time.time(),
            'words_per_second': 0,
            'elapsed_time': 0
        }

        found_password = None

        def check_password(password: str):
            if self.stop_cracking:
                return None

            self.stats['total_tested'] += 1
            self.stats['elapsed_time'] = time.time() - self.stats['start_time']

            # Actualizar velocidad
            if self.stats['elapsed_time'] > 0:
                self.stats['words_per_second'] = self.stats['total_tested'] / self.stats['elapsed_time']

            try:
                calculated_hash = self.hash_function(algorithm, password)
                if calculated_hash.lower() == target_hash.lower():
                    return password
            except Exception as e:
                logger.error(f"Error al calcular hash: {e}")
            return None

        try:
            # Usar hilos para procesamiento paralelo
            with ThreadPoolExecutor(max_workers=max_workers) as executor:
                futures = {executor.submit(check_password, word): word for word in wordlist}

                for future in as_completed(futures):
                    result = future.result()
                    if result:
                        found_password = result
                        self.stop_cracking = True
                        break

                    if self.stop_cracking:
                        break

        except Exception as e:
            logger.error(f"Error durante el cracking: {e}")
            return {
                'success': False,
                'password': None,
                'stats': self.stats,
                'error': str(e)
            }

        return {
            'success': found_password is not None,
            'password': found_password,
            'stats': self.stats
        }

    def stop_current_operation(self):
        """Detener operación actual"""
        self.stop_cracking = True
        logger.info("Operación de cracking detenida por el usuario")


# Singleton instance
cracker = AdvancedHashCracker()