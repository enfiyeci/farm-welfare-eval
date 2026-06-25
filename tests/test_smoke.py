def test_package_imports():
    import farm_eval

    assert hasattr(farm_eval, "__version__")
