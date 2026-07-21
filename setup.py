from setuptools import setup


setup(
    name="novavision-detection-transformation",
    version="0.1.0",
    description="Simple detection filtering and label-renaming component for NovaVision",
    install_requires=["sdk"],
    packages=[
        "novavision.detection_transformation",
        "novavision.detection_transformation.models",
        "novavision.detection_transformation.executors",
        "novavision.detection_transformation.utils",
    ],
    package_dir={"novavision.detection_transformation": "src"},
    python_requires=">=3.8",
)
