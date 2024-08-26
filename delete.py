def delete_old_files(currentdir, stpath):
    """
    This method deletes files from the specified directory (stpath) if they meet the criteria.
    Criteria: 
    - Files with creation time older than 'csixyrsc' 
    - Files with modification time older than 'mtwoyrsc'
    
    Parameters:
    - currentdir: The current directory.
    - stpath: The directory path where the files are located.
    """

    console = logging.StreamHandler()
    console.setLevel(logging.INFO)
    logging.basicConfig(level=logging.INFO, handlers=[console])

    setup_logger('log1', currentdir + '-old.txt')
    loggerOld = logging.getLogger('log1')
    
    setup_logger('log2', currentdir + '-current.txt')
    loggingCurrent = logging.getLogger('log2')
    
    setup_logger('log3', currentdir + '-error.txt')
    loggingError = logging.getLogger('log3')
    
    prfx = "\\\\UNC\\"
    stgpath = stpath + "/**/*"
    original_folder = Path(str(stgpath).replace('\\\\', prfx))

    # Retrieve and process files
    files = glob.iglob(str(stgpath), recursive=True)
    
    for filex in files:
        file = str(filex).replace('\\\\', prfx)
        
        if not os.path.isdir(file):
            extension = os.path.splitext(str(file))[1]
            try:
                # Check if the file meets the retention criteria
                if os.stat(file).st_ctime < csixyrsc and os.stat(file).st_mtime < mtwoyrsc:
                    # Fetch file details
                    ext = extension
                    z = Path(file).name
                    sz = str(os.path.getsize(str(file)))
                    on = io.owner(str(file))
                    cdt = str(datetime.fromtimestamp(os.stat(file).st_ctime))
                    mdt = str(datetime.fromtimestamp(os.stat(file).st_mtime))
                    adt = str(datetime.fromtimestamp(os.stat(file).st_atime))
                    er = ""

                    try:
                        os.remove(file)
                        loggingCurrent.info('%s|%s|%s|%s|%s|%s|Deleted', 
                                            sz, on, cdt, mdt, adt, str(file).replace("\\\\UNC\\", "\\"), er)
                    except Exception as e:
                        loggingError.info('%s|%s|%s|%s|%s|%s|%s|Error|%s', 
                                          sz, on, cdt, mdt, adt, str(file).replace("\\\\UNC\\", "\\"), er, str(e))
                        continue
            except OSError as ne:
                sz = ""
                on = ""
                cdt = ""
                mdt = ""
                adt = ""
                er = str(ne)
                loggingError.info('%s|%s|%s|%s|%s|%s|%s|Error|%s', 
                                  sz, on, cdt, mdt, adt, str(file).replace("\\\\UNC\\", "\\"), er)
                continue

    loggingError.handlers.clear()
    loggerOld.handlers.clear()
    loggingCurrent.handlers.clear()
    logging.shutdown()
