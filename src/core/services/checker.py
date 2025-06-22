import subprocess

from core.interfaces.init_command_base import DependencyChecker


class SystemDependencyChecker(DependencyChecker):
  def check_dependency(self, dependency: str) -> bool:
    try:
      subprocess.run([dependency, "--version"], capture_output=True, check=True)
      return True
    except (subprocess.CalledProcessError, FileNotFoundError):
      return False

  def install_dependency(self, dependency: str) -> bool:
    print(f"⚠️  {dependency} no está instalado. No se puede instalar automáticamente.")
    return False


class PythonDependencyChecker(DependencyChecker):
  def check_dependency(self, dependency: str) -> bool:
    try:
      subprocess.run(["python", "-m", "pip", "show", dependency], capture_output=True, check=True)
      return True
    except subprocess.CalledProcessError:
      return False

  def install_dependency(self, dependency: str) -> bool:
    try:
      subprocess.run(["python", "-m", "pip", "install", dependency], check=True)
      return True
    except subprocess.CalledProcessError:
      return False


class DependencyManager:
  def __init__(self):
    self.checkers = {"system": SystemDependencyChecker(), "python": PythonDependencyChecker()}

  def check_requirements(self, requirements: list[tuple[str, str]]) -> bool:
    all_ok = True
    for dep, dep_type in requirements:
      print(f"\n📍 Comprobando la dependencia {dep}")
      if not self.checkers[dep_type].check_dependency(dep):
        print(f"❌ Falta dependencia: {dep}")
        all_ok = False
        if not self._ask_and_install(dep, dep_type):
          return False
      else:
        print(f"✅ Dependencia {dep} encontrada")
    return all_ok

  def _ask_and_install(self, dependency: str, dep_type: str) -> bool:
    print(f"\n⚠️  Se requiere {dependency} para continuar.")
    answer = input("¿Deseas intentar instalarlo automáticamente? (s/n): ").lower()
    if answer == "s":
      return self.checkers[dep_type].install_dependency(dependency)
    return False
