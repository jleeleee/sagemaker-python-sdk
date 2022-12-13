from sagemaker.session import Session, NOTEBOOK_METADATA_FILE


class TensorBoardApp(object):
    """TensorBoardApp is a class for deploying a TensorBoard app."""

    def __init__(self, domain_id=None, user_profile_name=None, sagemaker_session=None):
        """Initialize a TensorBoardApp.

        Args:
            domain_id (str): The ID of the domain.
            user_profile_name (str): The name of the user profile.
            sagemaker_session (sagemaker.session.Session): Session object which
                manages interactions with Amazon SageMaker APIs and any other
                AWS services needed. If not specified, one is created using the
                default AWS configuration chain.
        """
        self.domain_id = domain_id
        self.user_profile_name = user_profile_name
        self.sagemaker_session = sagemaker_session or Session()

        if not domain_id or not user_profile_name:
            self._infer_domain_and_user()

    def _infer_domain_and_user(self):
        if not os.path.exists(NOTEBOOK_METADATA_FILE):
            return
        
        with open(NOTEBOOK_METADATA_FILE, "rb") as f:
            metadata = json.loads(f.read())
            instance_name = metadata["ResourceName"]
            domain_id = metadata.get("DomainId")
            user_profile_name = metadata.get("UserProfileName")
            if domain_id and user_profile_name:
                self.domain_id = domain_id
                self.user_profile_name = user_profile_name


    def get_signed_app_url(self, training_job_name=None):
        """Gets a signed URL to the TensorBoard app.

        Args:
            training_job_name (str): The name of the training job. If not
                specified, the training job name is read from the training job
                input configuration.

        Returns:
            str: A signed URL to the TensorBoard app.
        """
        response = self.sagemaker_session.sagemaker_client.create_presigned_domain_url(
            DomainId=self.domain_id,
            UserProfileName=self.user_profile_name
        )
        app_url = response['AuthorizedUrl']
        app_url += "&redirect=tensorboard"
        if training_job_name:
            app_url += "/add_folder_or_job/{}".format(training_job_name)

        return app_url