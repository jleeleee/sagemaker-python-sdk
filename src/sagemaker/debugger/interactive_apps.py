from sagemaker.session import Session


class TensorBoardApp(object):
    """TensorBoardApp is a class for deploying a TensorBoard app."""

    def __init__(self, domain_id, user_profile_name, sagemaker_session=None):
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

    def get_app_url(self, training_job_name=None):
        response = self.sagemaker_session.sagemaker_client.create_presigned_domain_url(
            DomainId=self.domain_id,
            UserProfileName=self.user_profile_name
        )
        app_url = response['AuthorizedUrl']response["AuthorizedUrl"]
        app_url += "&redirect=tensorboard"

        return app_url