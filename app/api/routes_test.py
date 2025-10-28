from fastapi import APIRouter, Response
from app.services.test_runner import TestRunner

router = APIRouter(prefix="/test", tags=["Tests"])

@router.post("/run")
def run_all_test(plain:bool = True):
    result = TestRunner.run_tests()
    
    if plain:
        log_output = (f"\n=== PYTEST EXECUTION ===\n\n"
                f"Exit code: {result['exit_code']}\n\n"
                f"{result['stdout']}\n{result['stderr']}"
        )
        return Response(content=log_output, media_type='text/plain; charset=utf-8')
    
    return {
            "exit_code": result["exit_code"],
            "stdout": result["stdout"],
            "stderr": result["stderr"]
    }